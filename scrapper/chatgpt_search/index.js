

// Function to add a sentence to the text area
function addSentence(sentence) {
  // Select the text area element
  const textarea = document.querySelector('#prompt-textarea');

  // Get the current content of the text area
  const currentContent = textarea.textContent;

  // Add the new sentence to the content
  const newContent = currentContent + ' ' + sentence;

  // Set the new content to the text area
  textarea.textContent = newContent;

  // Focus on the text area
  textarea.focus();
}



// Function to click the submit button
function clickSubmitButton() {

  // Select the submit button element
  const submitButton = document.querySelector('button[data-testid="send-button"]');
  submitButton.focus();
  // Trigger a click event on the button
  submitButton.click();
}

// Function to add sentence and submit
function addSentenceAndSubmit(sentence) {
  // Add the sentence
  addSentence(sentence);

  // Click submit button
  clickSubmitButton();
}

// Example usage:
// addSentenceAndSubmit("Hello, how are you?");
