document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('imageInput');
    const preview = document.getElementById('preview');
    const resultSection = document.getElementById('resultSection');
    const loading = document.querySelector('.loading');
    const birdImage = document.getElementById('birdImage');
    const birdName = document.getElementById('birdName');
    const birdDescription = document.getElementById('birdDescription');

    imageInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;

        // 顯示預覽圖片
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        reader.readAsDataURL(file);

        // 準備上傳資料
        const formData = new FormData();
        formData.append('image', file);

        // 顯示載入畫面
        loading.style.display = 'block';
        resultSection.style.display = 'none';

        try {
            // 修改後的 fetch URL
            const response = await fetch('/api/predict/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            loading.style.display = 'none';

            if (result.success) {
                birdName.textContent = result.bird.name;
                birdDescription.textContent = result.bird.description;
                birdImage.src = result.bird.image;
                
                const confidenceText = document.createElement('p');
                confidenceText.textContent = `辨識信心度: ${(result.confidence * 100).toFixed(2)}%`;
                confidenceText.className = 'confidence-text';
                birdDescription.appendChild(confidenceText);

                resultSection.style.display = 'block';
                resultSection.classList.add('show');
            } else {
                alert(result.message || '無法辨識圖片，請嘗試其他圖片');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('發生錯誤，請稍後再試');
            loading.style.display = 'none';
        }
    });

    // 其餘代碼保持不變...
});

const response = await fetch('/api/predict/', {
    method: 'POST',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
    body: formData
});