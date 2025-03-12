// Initialize PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';

let pdfDoc = null;
let pageNum = 1;
let canvas = null;
let ctx = null;
let scale = 1.5;

// Initialize the canvas when the document loads
document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById('pdfCanvas');
    ctx = canvas.getContext('2d');
});

// Handle file upload
document.getElementById('pdfFile').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
        const reader = new FileReader();
        reader.onload = function(e) {
            const typedarray = new Uint8Array(e.target.result);
            loadPDF(typedarray);
        };
        reader.readAsArrayBuffer(file);
    }
});

// Load the PDF
async function loadPDF(data) {
    try {
        pdfDoc = await pdfjsLib.getDocument({data: data}).promise;
        document.getElementById('pageInfo').textContent = `Page: ${pageNum} / ${pdfDoc.numPages}`;
        renderPage(pageNum);
    } catch (error) {
        console.error('Error loading PDF:', error);
        alert('Error loading PDF file');
    }
}

// Render the specified page
async function renderPage(num) {
    try {
        const page = await pdfDoc.getPage(num);
        const viewport = page.getViewport({scale: scale});

        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
            canvasContext: ctx,
            viewport: viewport
        };

        await page.render(renderContext).promise;
    } catch (error) {
        console.error('Error rendering page:', error);
        alert('Error rendering page');
    }
}

// Previous page button
document.getElementById('prevPage').addEventListener('click', () => {
    if (pdfDoc === null || pageNum <= 1) return;
    pageNum--;
    document.getElementById('pageInfo').textContent = `Page: ${pageNum} / ${pdfDoc.numPages}`;
    renderPage(pageNum);
});

// Next page button
document.getElementById('nextPage').addEventListener('click', () => {
    if (pdfDoc === null || pageNum >= pdfDoc.numPages) return;
    pageNum++;
    document.getElementById('pageInfo').textContent = `Page: ${pageNum} / ${pdfDoc.numPages}`;
    renderPage(pageNum);
});

// Download button
document.getElementById('downloadBtn').addEventListener('click', () => {
    if (canvas) {
        const dataUrl = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = 'edited-page.png';
        link.href = dataUrl;
        link.click();
    }
}); 