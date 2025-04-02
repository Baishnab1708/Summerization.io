let summaryCount = 0;

// DOM Elements
const fileBtn = document.getElementById('fileBtn');
const textBtn = document.getElementById('textBtn');
const fileArea = document.getElementById('fileArea');
const textArea = document.getElementById('textArea');
const textInput = document.getElementById('textInput');
const summarizeBtn = document.getElementById('summarizeBtn');
const lengthSlider = document.getElementById('lengthSlider');
const summaryOutput = document.getElementById('summaryOutput');
const summaryText = document.getElementById('summaryText');
const fileInput = document.getElementById('fileInput');
const loadingState = document.getElementById('loadingState');
const countElement = document.getElementById('summaryCount');
const starIcon = document.getElementById('starIcon');
const contactInfo = document.getElementById('contact-info');

function incrementSummaryCount() {
    summaryCount++;
    countElement.textContent = summaryCount;
    
    // Add animations
    countElement.classList.remove('count-increment');
    starIcon.classList.remove('pulse-animation');
    
    // Trigger reflow to restart animations
    void countElement.offsetWidth;
    void starIcon.offsetWidth;
    
    // Add animations back
    countElement.classList.add('count-increment');
    starIcon.classList.add('pulse-animation');
}

// Toggle between File and Text
fileBtn.addEventListener('click', () => {
    fileArea.classList.remove('hidden');
    document.getElementById('fileInputContainer').classList.remove('hidden');
    textArea.classList.add('hidden');
    fileBtn.classList.add('active');
    textBtn.classList.remove('active');
});

textBtn.addEventListener('click', () => {
    textArea.classList.remove('hidden');
    fileArea.classList.add('hidden');
    document.getElementById('fileInputContainer').classList.add('hidden');
    textBtn.classList.add('active');
    fileBtn.classList.remove('active');
});

// Drag and Drop Functionality
fileArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileArea.classList.add('dragging');
});

fileArea.addEventListener('dragleave', () => {
    fileArea.classList.remove('dragging');
});

fileArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileArea.classList.remove('dragging');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(files[0]);
        fileInput.files = dataTransfer.files;
    }
});

// Browse File Event
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
});

// Update the displayed slider value dynamically
lengthSlider.addEventListener('input', () => {
    const value = lengthSlider.value;
    document.getElementById('lengthLabel').textContent = `${value}%`;
});

// Summarize Button Click
summarizeBtn.addEventListener('click', async () => {
    const inputText = textInput.value.trim();
    const file = fileInput.files[0];
    const compressionRatio = lengthSlider.value / 100;
    
    if (!inputText && !file) {
        alert('Please enter text or upload a file.');
        return;
    }

    // Show loading state
    loadingState.classList.remove('hidden');
    summaryOutput.classList.add('hidden');

    const formData = new FormData();
    formData.append('compression_ratio', compressionRatio.toString());
    if (file) {
        formData.append('file', file);
    } else {
        formData.append('text', inputText);
    }

    console.log("Sending request to backend with compression ratio:", compressionRatio);

    try {
        const response = await fetch('https://BaishnabBehera-summerization-app.hf.space/summarize', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        console.log("Response received:", data);

        // Hide loading state
        loadingState.classList.add('hidden');

        if (response.ok) {
            summaryOutput.classList.remove('hidden');
            summaryText.textContent = data.summary;
            incrementSummaryCount(); // Increment the summary count

        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        loadingState.classList.add('hidden');
        alert('Failed to connect to backend.');
        console.error("Fetch error:", error);
    }
});

window.addEventListener('scroll', () => {
  const contactInfo = document.getElementById('contact-info');
  // Check if user is at the bottom of the page (with a 10px buffer)
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
    contactInfo.style.opacity = 1;
  } else {
    contactInfo.style.opacity = 0;
  }
});
