// Helper function to create a delay
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Helper function to click a button by selector
function clickButton(selector) {
  const button = document.querySelector(selector);
  if (button) {
      button.click();
  } else {
      console.error(`Button not found: ${selector}`);
  }
}

// Function to initialize the chat by clicking the "New chat" and "Web" buttons
function initializeChat() {
  // Click "New chat" button to start a new session
  clickButton('button[aria-label="New chat"]');
  
  // Wait 1-2 seconds for the page to load
  setTimeout(() => {
      // Click the "Web" button to enable web searching
      clickWebButton();
  }, 1500); // Adjust timeout based on network or page load time
}

// Function to click the "Web" button with the corrected selector
function clickWebButton() {
  const webButton = document.querySelector('button[aria-label="Search the web"]');
  if (webButton) {
      webButton.click();
  } else {
      console.error('Web button not found.');
  }
}

// Function to find the submit button reliably
async function findSubmitButton() {
  let submitButton = null;
  while (!submitButton) {
      submitButton = document.querySelector('button[data-testid="send-button"]');
      if (!submitButton) {
          console.log('Waiting for submit button to appear...');
          await sleep(500); // Wait for 500ms before checking again
      }
  }
  return submitButton;
}

// Helper function to add a question to the textarea
async function addSentence(sentence) {
  const textarea = document.querySelector('#prompt-textarea');
  textarea.textContent = ''; // Clear the textarea before adding the next question
  textarea.textContent = sentence; // Add the new question to the textarea
  textarea.focus();
  await sleep(500); // Wait for the textarea to update before proceeding
}

// Helper function to click the submit button
async function clickSubmitButton() {
  const submitButton = await findSubmitButton();
  submitButton.focus();
  submitButton.click();
}

// Wait for the response generation to finish by checking the "stop" button
async function waitForResponseToFinish() {
  let isGenerating = true;
  while (isGenerating) {
      const stopButton = document.querySelector('button[data-testid="stop-button"]');
      isGenerating = !!stopButton; // True if "Stop streaming" button is present
      await sleep(300); // Check every 300ms
  }
}

// Check if the system is currently generating a response
async function isResponseBeingGenerated() {
  const stopButton = document.querySelector('button[data-testid="stop-button"]');
  return !!stopButton; // Return true if the response is being generated
}

// Function to parse citations and search results separately
function parseCitationsAndResults() {
  const sources = {
      citations: [],
      searchResults: []
  };

  const mainContainer = document.querySelector('.flex.w-full.flex-col.border-t.border-token-border-light.bg-token-main-surface-primary');
  if (mainContainer) {
      const sections = mainContainer.querySelectorAll(':scope > div');

      sections.forEach(section => {
          const header = section.querySelector('div.sticky');
          if (header && header.innerText.includes("Citations")) {
              const citationItems = section.querySelectorAll('.flex.flex-col.px-3.py-2 > div');
              citationItems.forEach(citation => {
                  const linkElement = citation.querySelector('a');
                  const titleElement = citation.querySelector('div.line-clamp-2.text-sm.font-semibold');
                  const descriptionElement = citation.querySelector('div.line-clamp-2.text-sm.font-normal');

                  if (linkElement && titleElement && descriptionElement) {
                      sources.citations.push({
                          url: linkElement.href,
                          title: titleElement.innerText,
                          description: descriptionElement.innerText
                      });
                  }
              });
          } else if (header && header.innerText.includes("Search Results")) {
              const searchResultItems = section.querySelectorAll('.flex.flex-col.px-3.py-2 > div');
              searchResultItems.forEach(result => {
                  const linkElement = result.querySelector('a');
                  const titleElement = result.querySelector('div.line-clamp-2.text-sm.font-semibold');
                  const descriptionElement = result.querySelector('div.line-clamp-2.text-sm.font-normal');

                  if (linkElement && titleElement && descriptionElement) {
                      sources.searchResults.push({
                          link: linkElement.href,
                          title: titleElement.innerText,
                          description: descriptionElement.innerText
                      });
                  }
              });
          }
      });
  }

  return sources;
}

// Function to download JSON data as a file
function downloadJSON(data, filename) {
  const jsonData = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonData], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// Function to extract all human messages
async function extractHumanMessages() {
  const userMessages = new Set(); // Store user messages to track which questions have been processed

  const responses = document.querySelectorAll('article.w-full.text-token-text-primary');

  for (const element of responses) {
      const response = element;
      let textContent = response.innerText;

      if (response.querySelector('[data-message-author-role="user"]')) {
          // Remove "You said:\n" from the beginning of the text
          const userPrefix = "You said:\n";
          if (textContent.startsWith(userPrefix)) {
              textContent = textContent.slice(userPrefix.length);
          }
          userMessages.add(textContent); // Add the processed question to the set
      }
  }

  return userMessages; // Return the set of user messages
}

// Function to parse questions and responses
async function parseResponses() {
  const responseData = []; // Store the final data to save as JSONL

  const responses = document.querySelectorAll('article.w-full.text-token-text-primary');

  let currentQuestion = null;
  let currentId = null;
  let questionStartTime = null; // Variable to store the start time of the question

  for (const element of responses) {
    const response = element;
    let textContent = response.innerText;

    if (response.querySelector('[data-message-author-role="user"]')) {
      // Remove "You said:\n" from the beginning of the text
      const userPrefix = "You said:\n";
      if (textContent.startsWith(userPrefix)) {
        textContent = textContent.slice(userPrefix.length);
      }
      currentQuestion = textContent;
      currentId = questions.find(q => q.question === currentQuestion)?.id; // Find the corresponding ID
      questionStartTime = Date.now(); // Record the start time
    } else if (response.querySelector('[data-message-author-role="assistant"]') && currentQuestion) {
      // Remove "ChatGPT said:\nChatGPT\n\n" from the beginning of the text
      const unwantedPrefix = "ChatGPT said:\nChatGPT\n\n";
      if (textContent.startsWith(unwantedPrefix)) {
        textContent = textContent.slice(unwantedPrefix.length);
      }

      // Find the "Sources" button and click to get citations, if available
      const sourcesButton = response.querySelector('button.not-prose.group\\/footnote.mb-2.mt-3.flex.w-fit.items-center.gap-1\\.5.rounded-xl.border.border-token-border-light.bg-token-main-surface-primary.py-2.hover\\:bg-token-main-surface-secondary.pl-3.pr-2\\.5');
      let sources = { citations: [], searchResults: [] };

      if (sourcesButton) {
        sourcesButton.click();
        await sleep(1000); // Wait for the citations to load
        sources = parseCitationsAndResults(); // Parse the citations and search results
      }

      // Calculate response time
      const responseTime = Date.now() - questionStartTime; // Calculate the response time

      responseData.push({
        id: currentId,
        question: currentQuestion,
        result: textContent,
        search_results: sources.searchResults,
        response_time: responseTime
      });

      currentQuestion = null; // Reset the question for the next pair
    }
  }

  return responseData;
}

// Main function to submit questions within a specified range
async function submitAllQuestionsSequentially(questions, startIndex, endIndex) {
  let attempts = 0;
  let selectedQuestions = questions.slice(startIndex, endIndex + 1); // Select questions within the range
  let missingQuestions = selectedQuestions.map(q => q.question);

  while (missingQuestions.length > 0 && attempts < 5) {
      console.log(`Attempt ${attempts + 1}: Submitting questions...`);
      await sleep(1000);

      for (const element of missingQuestions) {
          const question = element;

          // Wait until the system is not generating a response
          while (await isResponseBeingGenerated()) {
              console.log('Waiting for current response to finish before submitting next question...');
              await sleep(1000); // Wait for 1 second before checking again
          }

          // Add the question to the textarea and wait before submitting
          await addSentence(question);

          // Click submit button
          await clickSubmitButton();

          // Wait for the response generation to finish
          await waitForResponseToFinish();

          // Wait before submitting the next question to avoid rate limiting
          await sleep(2000); // Adjust this based on your observation
      }

      // Wait for 7 seconds before starting to parse the responses
      console.log('Waiting for 7 seconds before parsing responses...');
      await sleep(7000);

      // After the last question's response is generated, extract human messages
      console.log('Extracting human messages to check for missing questions...');
      const processedQuestions = await extractHumanMessages();

      // Determine which questions are still missing
      missingQuestions = selectedQuestions
          .map(q => q.question)
          .filter(question => !processedQuestions.has(question));

      attempts++;
  }

  if (missingQuestions.length > 0) {
      console.warn('Some questions could not be submitted after 5 attempts:', missingQuestions);
  } else {
      console.log('All questions submitted successfully.');
  }

  // Parse responses and download the result with the specified filename format
  console.log('Parsing responses and downloading results...');
  const responseData = await parseResponses();
  downloadJSON(responseData, `Chatgpt_search_${startIndex}_${endIndex}.jsonl`);
}

// Function to submit questions in batches
async function submitQuestionsInBatches(questions, startIndex, batchSize) {
  let currentIndex = startIndex;

  while (currentIndex < questions.length) {
    const endIndex = Math.min(currentIndex + batchSize - 1, questions.length - 1);

    console.log(`Submitting questions from index ${currentIndex} to ${endIndex}...`);

    // Initialize chat before processing each batch
    initializeChat();

    // Submit questions for the current batch
    await submitAllQuestionsSequentially(questions, currentIndex, endIndex);

    // Move to the next batch
    currentIndex += batchSize;
  }

  console.log('All batches processed successfully.');
}

// Start the question submission and parsing process with specified indices and batch size
// const batchSize = 30; // Define your batch size
// submitQuestionsInBatches(questions, 0, batchSize); // Example: start from index 0 with a batch size of 5