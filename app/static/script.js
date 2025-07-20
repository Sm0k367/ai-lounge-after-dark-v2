document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const uploadButton = document.getElementById('uploadButton');
    const fileNameSpan = document.getElementById('fileName');
    const generateButton = document.getElementById('generateButton');
    const statusDiv = document.getElementById('status');
    const videoSection = document.getElementById('video-section');
    const videoPlayer = document.getElementById('videoPlayer');
    const downloadLink = document.getElementById('downloadLink');

    let selectedFile = null;

    // Trigger file input click when upload button is clicked
    uploadButton.addEventListener('click', () => {
        imageUpload.click();
    });

    // Handle file selection
    imageUpload.addEventListener('change', (event) => {
        selectedFile = event.target.files[0];
        if (selectedFile) {
            fileNameSpan.textContent = selectedFile.name;
            generateButton.disabled = false;
            setStatus('Ready to generate. Click "Generate Video".', '');
            videoSection.classList.add('hidden'); // Hide video section if new file selected
            videoPlayer.src = ''; // Clear previous video
            downloadLink.style.display = 'none'; // Hide download link
        } else {
            fileNameSpan.textContent = 'No file chosen';
            generateButton.disabled = true;
            setStatus('Please select an image file.', 'error');
        }
    });

    // Handle video generation
    generateButton.addEventListener('click', async () => {
        if (!selectedFile) {
            setStatus('Please select an image file first.', 'error');
            return;
        }

        setStatus('Generating video... This may take a few moments.', 'loading');
        generateButton.disabled = true;
        uploadButton.disabled = true;

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('/api/generate', { // Updated API endpoint
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                if (data.video_url) {
                    videoPlayer.src = data.video_url;
                    videoSection.classList.remove('hidden');
                    downloadLink.href = data.video_url;
                    downloadLink.style.display = 'inline-block';
                    setStatus('Video generated successfully!', 'success');
                } else {
                    throw new Error('Video URL not received from server.');
                }
            } else if (response.status === 202 && data.status === 'loading') {
                // Handle model loading status
                setStatus(`Model is loading: ${data.message}. Please wait and try again in ~30 seconds.`, 'loading');
                // Re-enable buttons after a short delay to allow user to retry
                setTimeout(() => {
                    generateButton.disabled = false;
                    uploadButton.disabled = false;
                }, 30000); // Re-enable after 30 seconds
            } else {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error('Generation error:', error);
            setStatus(`Error: ${error.message}. Please try again.`, 'error');
            videoSection.classList.add('hidden');
            videoPlayer.src = '';
            downloadLink.style.display = 'none';
        } finally {
            // Only re-enable if not in a loading state
            if (statusDiv.classList.contains('loading') === false) {
                generateButton.disabled = false;
                uploadButton.disabled = false;
            }
        }
    });

    // Function to update status message
    function setStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = 'status-message'; // Reset classes
        if (type) {
            statusDiv.classList.add(type);
        }
    }

    // Initial status message
    setStatus('Upload an image to begin your cybernetic vision.', '');
});