async function submitFollowUp(followUpText) {
    const textAreaElement = document.querySelector(".overflow-auto");
    const submitButton = document.querySelector("button[aria-label='Submit']");

    submitButton.disabled = false;

    textAreaElement.focus();
    textAreaElement.select();

    document.execCommand('insertText', false, followUpText);

    setTimeout(() => {
        submitButton.click();
    }, 100);

    let rewriteButton = undefined;
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    while (rewriteButton === undefined) {
        const buttons = document.querySelectorAll('button.focus-visible\\:bg-offsetPlus.dark\\:focus-visible\\:bg-offsetPlusDark.md\\:hover\\:bg-offsetPlus.text-textOff.dark\\:text-textOffDark.md\\:hover\\:text-textMain.dark\\:md\\:hover\\:bg-offsetPlusDark.dark\\:md\\:hover\\:text-textMainDark.font-sans.focus\\:outline-none.outline-none.outline-transparent.transition.duration-300.ease-out.font-sans.select-none.items-center.relative.group\\/button.justify-center.text-center.items-center.rounded-full.cursor-point.active\\:scale-\\[0\\.97\\].active\\:duration-150.active\\:ease-outExpo.origin-center.whitespace-nowrap.inline-flex.text-sm.px-sm.font-medium.h-8');
        rewriteButton = Array.from(buttons).find(button => button.textContent.includes('Rewrite'));
        await sleep(200);
    }

    const viewMoreSrcsButton = document.querySelector('.flex.h-full.max-h-\\[190px\\].w-\\[40vw\\].cursor-pointer.flex-col.justify-between.gap-1.rounded-lg.p-sm.md\\:w-auto.border-borderMain\\/50.ring-borderMain\\/50.divide-borderMain\\/50.dark\\:divide-borderMainDark\\/50.dark\\:ring-borderMainDark\\/50.dark\\:border-borderMainDark\\/50.transition.duration-300.bg-offset.dark\\:bg-offsetDark.md\\:hover\\:bg-offsetPlus.md\\:dark\\:hover\\:bg-offsetPlusDark');
    let srcs = [];

    if (viewMoreSrcsButton) {
        viewMoreSrcsButton.click();

        while (document.querySelector('div.flex.h-full.flex-col.items-start.gap-md.border-borderMain\\/50.ring-borderMain\\/50.divide-borderMain\\/50.dark\\:divide-borderMainDark\\/50.dark\\:ring-borderMainDark\\/50.dark\\:border-borderMainDark\\/50.bg-transparent') === null) {
            await sleep(200);
        }

        const sources = document.querySelector('div.flex.h-full.flex-col.items-start.gap-md.border-borderMain\\/50.ring-borderMain\\/50.divide-borderMain\\/50.dark\\:divide-borderMainDark\\/50.dark\\:ring-borderMainDark\\/50.dark\\:border-borderMainDark\\/50.bg-transparent');
        let times = 0;
        while (sources.children.length === 0 && times < 10) {
            times += 1;
            await sleep(200);
        }

        for (let i = 0; i < sources.children.length; i++) {
            srcs.push(sources.children[i].children[0].children[0].href);
        }
    }

    const answerTextElement = document.querySelector(".mb-md .prose");
    const answerText = [...answerTextElement.textContent.trim()].join("");


    if (viewMoreSrcsButton) {
        document.querySelector('button[data-testid="close-modal"].focus-visible\\:bg-offsetPlus').click();
        await sleep(200);
    }

    document.querySelector('button.focus-visible\\:bg-offsetPlus').click();
    await sleep(200);
    document.querySelectorAll('div.select-none.rounded.transition-all.duration-300.py-md.px-sm.-ml-sm.md\\:p-sm.md\\:ml-0.md\\:h-full.md\\:hover\\:bg-offsetPlus.md\\:hover\\:dark\\:bg-offsetPlusDark.cursor-pointer.rounded')[1].click()
    await sleep(500);


    document.querySelector('button.bg-superAlt.text-white.hover\\:opacity-50').click();
    await sleep(3000);

    return { srcs, answerText };
}




function download_results(input, filename) {
    const content = JSON.stringify(input, null, 2);
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

function decodeUnicode(str) {
    return str.replace(/\\u[\dA-Fa-f]{4}/g, (match) => String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16)));
}

async function main(queries, startIndex, endIndex) {
    let results = [];
    let downloadedQueries = new Set();

    try {
        const existingResults = JSON.parse(localStorage.getItem('perplexity_results')) || [];
        existingResults.forEach(res => downloadedQueries.add(res.query));
        results = existingResults;
        console.log("Loaded existing results:", results.length);
    } catch (e) {
        console.error("Error loading existing results:", e);
    }

    startIndex = Math.max(0, startIndex);
    endIndex = Math.min(queries.length - 1, endIndex);

    for (let i = startIndex; i <= endIndex; i++) {
        let query = decodeURIComponent(escape((queries[i].question)));

        if (downloadedQueries.has(query)) {
            console.log(`Skipping already downloaded query ${i + 1}: ${query}`);
            continue;
        }

        console.log(`Processing query ${i + 1}: ${query}`);

        try {
            const { srcs, answerText } = await submitFollowUp(query);
            results.push({ query, srcs, answerText });
            downloadedQueries.add(query);

            if ((i - startIndex + 1) % 15 === 0 || i === endIndex) {
                const start = i - ((i - startIndex) % 15) ;
                const end = Math.min(i, start + 14);

                const filename = `pplx_results_${start + 1}_${end + 1}.json`;
                download_results({ results: results.slice(results.length - (end - start + 1)) }, filename);
                localStorage.setItem('perplexity_results', JSON.stringify(results));
                console.log(`Downloaded ${end - start + 1} results to ${filename}`);
            }

        } catch (error) {
            console.error(`Error processing query ${i + 1}: ${query}`, error);
        }
    }
}
