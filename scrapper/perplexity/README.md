
## Running Instructions:

### Perplexity AI Scraper

1. **Prerequisites:**  Ensure you are logged into your Perplexity AI account in your browser.

2. **Open Developer Tools:** Open your browser's developer tools by pressing F12.

3. **Navigate to Console:** Select the "Console" tab within the developer tools.

4. **Copy and Paste Scraper Code:** Copy the contents of the `scrapper/perplexity/index.js` file and paste it into the browser's console.

5. **Define Queries:** Define the `queries` variable in the console. This should be an array of JSON objects, each containing an `id`, `question`, and `expected_answer`.  Example:

   ```javascript
   queries = [
       {"id": "40ca4c4f-cad5-40b5-87d6-33a18e58d13e", "question": "does airbus manufacture the nh90 helicopter", "expected_answer": "This question is somewhat misleading. While Airbus is involved with the NH90, it does not directly manufacture it. Airbus owns 62.5% of NHIndustries, the joint venture that produces the NH90. Saying Airbus manufactures it directly would be an oversimplification."},
       {"id": "d6f9a4b9-457b-4cfb-8757-fa189acc4cc2", "question": "Russian attack on Kyiv Oblast casualties", "expected_answer": "The Russian attack on Kyiv Oblast killed 2 people, including a 4-year-old boy."},
       {"id": "e3648e57-1e81-4904-bc54-5f1fe70da908", "question": "Gone with the Wind production cost", "expected_answer": "The production cost of 'Gone with the Wind' was reported to be between $3.9 million and $4.25 million."}
   ];
   ```

6. **Run the Scraper:** Execute the `main` function in the console, providing three arguments:

   * `queries`: The array of query objects defined in step 5.
   * `startIndex`: The index of the first query to process (inclusive).
   * `endIndex`: The index of the last query to process (inclusive).

   Example: `main(queries, 0, 2)` will process the first three queries.


7. **Downloaded Results:** The scraper will download results in batches of 15 (or fewer, if the end of the query list is reached) to JSON files named `pplx_results_[start]_to_[end].json`.  It also stores results in local storage to resume progress if interrupted.
