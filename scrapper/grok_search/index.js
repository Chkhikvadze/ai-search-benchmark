// Helper function to create a delay
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Function to check if the model is currently generating a response
async function isResponseBeingGenerated() {
  const loadingButton = document.querySelector('button[aria-label="Cancel"]');
  return !!loadingButton;
}

// Helper function to add a question to the textarea
async function addQuestion(question) {
  const textarea = document.querySelector('textarea[placeholder="Ask anything"]');
  textarea.value = ""; // Clear the textarea
  textarea.focus();
  textarea.select();
  document.execCommand("insertText", false, question);
  textarea.focus();
  await sleep(500);
}

// Helper function to click the submit button
function clickSubmitButton() {
  const submitButton = document.querySelector('button[aria-label="Grok something"]');
  if (submitButton) {
    submitButton.click();
  } else {
    console.error("Submit button not found.");
  }
}

// Helper function to get the last response
function getLastResponse() {
  const elements = Array.from(document.querySelectorAll("span")).filter((el) =>
    el.textContent.includes("Answer")
  );
  const answerElement =
    elements[elements.length - 1].parentElement.parentElement.parentElement
      .children[1];
  return answerElement.textContent;
}

// Helper function to extract link elements
function extractlinkElement(element) {
  const linkElements = element.querySelectorAll('a[href]');

  for (const linkElement of linkElements) {
    const href = linkElement.href;
    
    if (href.startsWith("https://x.com") || href.startsWith("https://twitter.com")) {
      const match = href.match(/\/status\/(\d+)\//);
      if (match) {
        const baseUrl = href.substring(0, match.index + match[0].length);
        return baseUrl;
      }
    } else if (href.startsWith("/")) {
      const fullLink = window.location.origin + href;
      if(fullLink.startsWith("https://x.com") || fullLink.startsWith("https://twitter.com")) {
        const match = fullLink.match(/\/status\/(\d+)\//);
        if(match) {
          const baseUrl = fullLink.substring(0, match.index + match[0].length);
          return baseUrl;
        }
      }
    }
  }
  return '';
}


// Helper function to get search results
function getSearchResults() {
  try {
    const elements = Array.from(document.querySelectorAll('span')).filter(el => 
      el.textContent.includes('Answer')
    );
    const results = [];
    
    if (elements.length === 0) {
      console.warn('No Answer elements found');
      return [];
    }
    
    const lastElement = elements[elements.length - 1];
    if (!lastElement?.parentElement?.parentElement?.parentElement?.parentElement) {
      console.warn('Required parent elements not found');
      return [];
    }
    
    const parentContainer = lastElement.parentElement.parentElement.parentElement.parentElement;
    
    if (parentContainer.childElementCount > 2) {
      try {
        const sources = parentContainer.children[1].children[0].children[0].children[1].children[0].children;
        
        for (const element of sources) {
          try {
            const link = extractlinkElement(element);
            if (link) {
              const description = element.firstChild?.children[1]?.children[0]?.children[1]?.textContent || '';
              results.push({
                url: link,
                description: description
              });
            }
          } catch (sourceError) {
            console.warn('Error processing individual source:', sourceError);
            continue; // Skip this source and continue with others
          }
        }
      } catch (sourcesError) {
        console.warn('Error accessing sources container:', sourcesError);
        return [];
      }
    }
    
    return results;
  } catch (error) {
    console.error('Error in getSearchResults:', error);
    return []; // Return empty array in case of any error
  }
}

// Helper function to download results
function downloadResults(results, startIndex, endIndex) {
  const dataStr = JSON.stringify(results, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `grok_${startIndex}_${endIndex}_result.jsonl`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Helper function to click the New Chat button
function clickNewChatButton() {
  const newChatButton = document.querySelector('button[aria-label="New Chat"]');
  if (newChatButton) {
    newChatButton.click();
    console.log("Started new chat");
  } else {
    console.error("New Chat button not found");
  }
}

// Main function to submit questions sequentially
async function submitQuestionsSequentially(questions) {
  const results = [];

  for (const questionObj of questions) {

    // Wait until system is ready
    while (await isResponseBeingGenerated()) {
      console.log("Waiting for system to be ready...");
      await sleep(1000);
    }

    // Add the question and submit
    await addQuestion(questionObj.question);
    const startTime = performance.now();
    clickSubmitButton();
    await sleep(1000);

    // Wait for response generation to finish
    while (await isResponseBeingGenerated()) {
      await sleep(300);
    }

    const endTime = performance.now();
    const responseTime = (endTime - startTime) / 1000;

    await sleep(300);
    // Get the response and search results
    const response = getLastResponse();
    await sleep(300);
    const searchResults = getSearchResults();
    
    // Store the result
    results.push({
      id: questionObj.id,
      question: questionObj.question,
      result: response,
      search_results: searchResults,
      response_time: responseTime
    });

    // Log progress
    console.log(`ID: ${questionObj.id}`);
    console.log(`Question: "${questionObj.question}"`);
    console.log(`Response: "${response}"`);
    console.log(`Response time: ${responseTime.toFixed(2)} seconds`);
    console.log('Sources:', searchResults);
    console.log('-------------------');

    await sleep(2000);
  }

  console.log("All questions processed successfully.");
  console.log("Final results:", results);
  return results;
}

// Function to submit questions in batches
async function submitQuestionsInBatches(questions, startIndex, endIndex, batchSize = 30) {
  let currentIndex = startIndex;

  while (currentIndex < endIndex) {
    const batchEndIndex = Math.min(currentIndex + batchSize - 1, endIndex);
    
    console.log(`Processing batch from index ${currentIndex} to ${batchEndIndex}...`);
    
    // Get questions for current batch
    const batchQuestions = questions.slice(currentIndex, batchEndIndex + 1);
    
    // Start new chat for each batch
    clickNewChatButton();
    await sleep(1000);
    
    // Process the batch
    const batchResults = await submitQuestionsSequentially(batchQuestions);
    
    // Download results for this batch with the new naming convention
    downloadResults(batchResults, currentIndex, batchEndIndex);
    
    // Move to next batch
    currentIndex = batchEndIndex + 1;
    
    // Wait between batches
    await sleep(2000);
  }

  console.log(`Completed processing all questions from index ${startIndex} to ${endIndex}`);
}

// Example usage:

// Process questions from index 0 to 100 in batches of 30
// submitQuestionsInBatches(questions, 0, questions.length-1, 30)
//   .then(() => console.log("All batches processed successfully."))
//   .catch((error) => console.error("Error processing batches:", error));
