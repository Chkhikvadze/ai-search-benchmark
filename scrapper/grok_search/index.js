// Helper function to create a delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  // Function to check if the model is currently generating a response
  async function isResponseBeingGenerated() {
    const loadingButton = document.querySelector('button[aria-label="Cancel"]');
    return !!loadingButton; // Return true if the loading button is present
  }
  
  // Helper function to add a sentence to the textarea
  async function addSentence(sentence) {
    const textarea = document.querySelector('textarea[placeholder="Ask anything"]');
    textarea.value = ''; // Clear the textarea before adding the next sentence

    // Simulate user input by setting the value and dispatching input events
    textarea.focus();
    textarea.select();

    document.execCommand('insertText', false, sentence);


    textarea.focus();
    await sleep(500); // Wait for the textarea to update before proceeding
  }
  
  // Helper function to click the submit button
  function clickSubmitButton() {
    const submitButton = document.querySelector('button[aria-label="Grok something"]');
    if (submitButton) {
      submitButton.click();
    } else {
      console.error('Submit button not found.');
    }
  }
  
  // Main function to submit a list of sentences sequentially
  async function submitSentencesSequentially(sentences) {
    for (const sentence of sentences) {
      // Wait until the system is not generating a response
      while (await isResponseBeingGenerated()) {
        console.log('Waiting for current response to finish before submitting next sentence...');
        await sleep(1000); // Wait for 1 second before checking again
      }
  
      // Add the sentence to the textarea and wait before submitting
      await addSentence(sentence);
  
      // Click submit button
      clickSubmitButton();
  
      // Wait for the response generation to finish
      while (await isResponseBeingGenerated()) {
        await sleep(300); // Check every 300ms
      }
  
      // Wait before submitting the next sentence to avoid rate limiting
      await sleep(2000); // Adjust this based on your observation
    }
  
    console.log('All sentences submitted successfully.');
  }

// Example usage
const sentences = [
"What is the capital of France?",
"How does photosynthesis work?",
"Explain the theory of relativity."
];

submitSentencesSequentially(sentences)
.then(() => console.log('Example sentences submitted.'))
.catch(error => console.error('Error submitting sentences:', error));