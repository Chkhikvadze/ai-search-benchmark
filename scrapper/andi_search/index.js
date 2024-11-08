async function submitQuestionAndExtractMessages(inputObject) {
    // Function to delay execution for a specified time (in ms)
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Destructure the question from the input object
    const { id, question } = inputObject;

    // Input the question into the text area
    const textAreaElement = document.querySelector(".rcw-input[contenteditable='true']");
    textAreaElement.focus();
    document.execCommand('insertText', false, question);

    // Click the submit button
    const submitButton = document.querySelector("button.rcw-send");
    submitButton.click();

    // Wait for 1 second to allow the UI to update
    await sleep(500);

    // Start timing the response
    const startTime = Date.now();

    // Wait for the loading icon to appear and then disappear
    await waitForLoadingToFinish();

    // End timing the response
    const endTime = Date.now();

    // Wait for an additional 0.5 seconds to ensure the response is fully loaded
    await sleep(500);
    const responseTime = endTime - startTime;

    // Extract messages
    const messages = extractMessages();

    // Extract references if the special button is present
    let references = [];
    const messagesContainer = document.querySelector("#messages");

    // Select all message elements within the container
    const messageElements = messagesContainer.querySelectorAll(".rcw-message");

    const responseElement = messageElements[messageElements.length - 1]

    const specialButton = responseElement.querySelector('.ui.blue.big.circular.icon.right.floated.button');
    if (specialButton) {
        references = await extractReferences();
    }

    // Construct the result object
    const result = {
        id: id,
        question: question,
        result: messages[messages.length - 1].text,
        search_results: references,
        response_time: responseTime / 1000.0
    };

    console.log('Result:', result);
    return result;
}

async function waitForLoadingToFinish() {
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    let loadingIconExists = true;

    // Wait until the loading icon disappears
    while (loadingIconExists) {
        const loaderElement = document.querySelector('.loader.active');
        loadingIconExists = !!loaderElement;
        await sleep(100);
    }
}


async function extractReferences() {
    const referenceComponents = document.querySelectorAll('.lw-feed-results');

    const references = Array.from(referenceComponents).map(component => {
        const titleElement = component.querySelector('.header.lw-card-image-header a');
        const descriptionElement = component.querySelector('.description div');
        const linkElement = component.querySelector('.meta.lw-citation-button');

        return {
            title: titleElement ? titleElement.textContent.trim() : null,
            description: descriptionElement ? descriptionElement.textContent.trim() : null,
            url: linkElement ? linkElement.textContent.trim() : null
        };
    });

    return references;
}

function extractMessages() {
    // Select the container holding all messages
    const messagesContainer = document.querySelector("#messages");

    // Select all message elements within the container
    const messageElements = messagesContainer.querySelectorAll(".rcw-message");

    // Initialize an array to store the extracted messages
    const messages = [];

    // Iterate over each message element
    messageElements.forEach(messageElement => {
        // Find the first paragraph within the message element
        const paragraphElement = messageElement.querySelector("p");

        // Extract and store the message text
        if (paragraphElement) {
            messages.push({ type: "response", text: paragraphElement.textContent.trim() });
        }
    });

    // Return the list of messages
    return messages;
}

function downloadResults(content, filename) {
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function main(queries, startIndex, endIndex) {
    let results = [];

    for (let i = startIndex; i <= endIndex; i++) {
        const inputObject = queries[i];

        console.log(`Processing query ${i + 1}: ${inputObject.question}`);

        try {
            const result = await submitQuestionAndExtractMessages(inputObject);
            results.push(result);

            // Log the formatted result
            console.log(`Formatted result for query ${i + 1}:`, JSON.stringify(result, null, 2));


        } catch (error) {
            console.error(`Error processing query ${i + 1}: ${inputObject.question}`, error);
        }
    }

    // Create a filename with the format andi_startindex_endindex.jsonl
    const filename = `andi_${startIndex}_${endIndex}.jsonl`;

    // Download the results as a JSONL file
    const jsonlContent = results.map(result => JSON.stringify(result)).join('\n');

    console.log(`Final results: ${jsonlContent}`);
    downloadResults(jsonlContent, filename);
}