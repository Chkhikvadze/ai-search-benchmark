// Sample questions array to automate
const questions = [
  {"id": "90589bcc-c99e-42ad-8dd6-35b1e12a18c1", "question": "why did oracle discontinue java development after sun microsystems acquisition"},
  {"id": "1a49b8ad-67ee-4027-a75c-754adb4eadc8", "question": "express bus fare cost nyc"},
  {"id": "797d8c64-6772-4d11-bd75-ce99cbb6bac2", "question": "ukrain destroyed what type of russian ship?"},
  {"id": "c474b8b5-1c9d-4957-9506-7ba00ec7d701", "question": "What was the significance of the Boeing 747's first flight?"},
  {"id": "4d353679-d1ae-4c94-b51c-066f1213d931", "question": "What is the refund policy for the Learn Enough tutorials?"}
];

// Utility to delay execution for a specified time (in ms)
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Helper to click a button by its selector
function clickButton(selector) {
  const button = document.querySelector(selector);
  if (button) {
      button.click();
  } else {
      console.error(`Button not found: ${selector}`);
  }
}

// Initializes a new chat session and enables web search
function initializeChat() {
  clickButton('button[aria-label="New chat"]'); // Starts a new chat session
  setTimeout(clickWebButton, 1500); // Enables web search after a brief delay
}

// Clicks the "Web" button if available
function clickWebButton() {
  const webButton = document.querySelector('button[aria-label="Search the web"]');
  if (webButton) {
      webButton.click();
  } else {
      console.error('Web button not found.');
  }
}

// Repeatedly checks for the presence of the submit button, then returns it
async function findSubmitButton() {
  let submitButton = null;
  while (!submitButton) {
      submitButton = document.querySelector('button[data-testid="send-button"]');
      if (!submitButton) {
          console.log('Waiting for submit button to appear...');
          await sleep(500);
      }
  }
  return submitButton;
}

// Adds a question to the textarea input, focusing it after updating
async function addSentence(sentence) {
  const textarea = document.querySelector('#prompt-textarea');
  textarea.textContent = '';
  textarea.textContent = sentence;
  textarea.focus();
  await sleep(500); // Short delay for textarea to update
}

// Submits the question by clicking the submit button
async function clickSubmitButton() {
  const submitButton = await findSubmitButton();
  submitButton.focus();
  submitButton.click();
}

// Waits until the response generation completes by checking for the "Stop" button
async function waitForResponseToFinish() {
  while (document.querySelector('button[data-testid="stop-button"]')) {
      await sleep(300); // Short interval check
  }
}

// Checks if a response is currently being generated
async function isResponseBeingGenerated() {
  return !!document.querySelector('button[data-testid="stop-button"]');
}

// Parses citations and search results in the response
function parseCitationsAndResults() {
  const sources = { citations: [], searchResults: [] };
  const mainContainer = document.querySelector('.flex.w-full.flex-col.border-t.border-token-border-light.bg-token-main-surface-primary');

  if (mainContainer) {
      mainContainer.querySelectorAll(':scope > div').forEach(section => {
          const header = section.querySelector('div.sticky');
          if (header) {
              const items = section.querySelectorAll('.flex.flex-col.px-3.py-2 > div');
              items.forEach(item => {
                  const linkElement = item.querySelector('a');
                  const titleElement = item.querySelector('div.line-clamp-2.text-sm.font-semibold');
                  const descriptionElement = item.querySelector('div.line-clamp-2.text-sm.font-normal');
                  
                  if (linkElement && titleElement && descriptionElement) {
                      const entry = {
                          link: linkElement.href,
                          title: titleElement.innerText,
                          description: descriptionElement.innerText
                      };

                      if (header.innerText.includes("Citations")) {
                          sources.citations.push(entry);
                      } else if (header.innerText.includes("Search Results")) {
                          sources.searchResults.push(entry);
                      }
                  }
              });
          }
      });
  }
  return sources;
}

// Downloads JSON data as a file with a given filename
function downloadJSON(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// Parses and downloads responses for each question
async function parseResponses() {
  const responseData = {};
  const responses = document.querySelectorAll('article.w-full.text-token-text-primary');
  let currentQuestion = null;

  for (const response of responses) {
      let textContent = response.innerText;
      
      // Check if it's a user or assistant message
      if (response.querySelector('[data-message-author-role="user"]')) {
          currentQuestion = textContent;
      } else if (response.querySelector('[data-message-author-role="assistant"]') && currentQuestion) {
          textContent = textContent.replace("ChatGPT said:\nChatGPT\n\n", "");

          // Get sources if available
          const sourcesButton = response.querySelector('button.not-prose.group\\/footnote.mb-2.mt-3.flex.w-fit.items-center.gap-1\\.5.rounded-xl.border.border-token-border-light.bg-token-main-surface-primary.py-2.hover\\:bg-token-main-surface-secondary.pl-3.pr-2\\.5');
          let sources = { citations: [], searchResults: [] };

          if (sourcesButton) {
              sourcesButton.click();
              await sleep(1000); // Wait for citations to load
              sources = parseCitationsAndResults();
          }

          responseData[currentQuestion] = { text: textContent, sources };
          currentQuestion = null;
      }
  }
  downloadJSON(responseData, 'response.json');
}

// Submits all questions in sequence with appropriate delays
async function submitAllQuestionsSequentially(questions) {
  await sleep(1000);
  for (const { question } of questions) {
      while (await isResponseBeingGenerated()) {
          console.log('Waiting for current response to finish...');
          await sleep(1000);
      }

      await addSentence(question);
      await clickSubmitButton();
      await waitForResponseToFinish();
      await sleep(2000); // Adjust delay based on rate limits
  }

  console.log('Waiting briefly before parsing responses...');
  await sleep(7000);
  console.log('All questions submitted. Parsing responses now...');
  await parseResponses();
}

// Starts the question submission and parsing process
// initializeChat();
// submitAllQuestionsSequentially(questions);