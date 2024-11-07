
## Running Instructions:

### ChatGPT Search Scraper

1. **Prerequisites:** Ensure you are logged into your ChatGPT account at chatgpt.com. Note that a ChatGPT Plus plan is required.

2. **Open Developer Tools:** Open your browser's developer tools by pressing F12.

3. **Navigate to Console:** Select the "Console" tab within the developer tools.

4. **Copy and Paste Scraper Code:** Copy the contents of the `scrapper/chatgpt_search/index.js` file and paste it into the browser's console.

5. **Define Questions:** Define the `questions` array in the console. This should be an array of JSON objects, each containing an `id` and `question`. Example:

   ```javascript
   questions = [
       { "id": "90589bcc-c99e-42ad-8dd6-35b1e12a18c1", "question": "why did oracle discontinue java development after sun microsystems acquisition" },
       { "id": "1a49b8ad-67ee-4027-a75c-754adb4eadc8", "question": "express bus fare cost nyc" },
       { "id": "797d8c64-6772-4d11-bd75-ce99cbb6bac2", "question": "ukrain destroyed what type of russian ship?" },
       { "id": "c474b8b5-1c9d-4957-9506-7ba00ec7d701", "question": "What was the significance of the Boeing 747's first flight?" }
   ];
   ```

6. **Run the Scraper:** Execute the `submitAllQuestionsSequentially` function in the console, providing the `questions` array as the input. This will initiate the scraping engine.

   Example: `submitAllQuestionsSequentially(questions);`

7. **Downloaded Results:** After the scraping process completes, the results will be automatically downloaded as a JSON file.
