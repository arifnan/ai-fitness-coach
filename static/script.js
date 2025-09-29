document.addEventListener('DOMContentLoaded', () => {

    // --- LOGIKA UNTUK SEMUA SLIDER ---

    // 1. Slider Utama di Halaman Home
    let heroSlideIndex = 0;
    showHeroSlides();

    function showHeroSlides() {
        const slides = document.querySelectorAll(".slider-container .slide");
        if (slides.length === 0) return; // Keluar jika tidak di Halaman Home
        slides.forEach(slide => slide.style.display = "none");
        heroSlideIndex++;
        if (heroSlideIndex > slides.length) { heroSlideIndex = 1 }
        slides[heroSlideIndex - 1].style.display = "block";
        setTimeout(showHeroSlides, 4000); // Ganti gambar setiap 4 detik
    }

    // 2. Slider Individual untuk Setiap Proyek di Halaman About
    const projectSliders = document.querySelectorAll('.project-slider-container');
    projectSliders.forEach(slider => {
        let slideIndex = 0;
        const slides = slider.querySelectorAll('.project-image-slide');
        
        function showProjectSlides() {
            if (slides.length === 0) return;
            slides.forEach(slide => slide.style.display = "none");
            slideIndex++;
            if (slideIndex > slides.length) { slideIndex = 1; }
            slides[slideIndex - 1].style.display = "block";
            setTimeout(showProjectSlides, 3500); // Ganti gambar proyek setiap 3.5 detik
        }
        showProjectSlides();
    });

    // --- LOGIKA UNTUK CHAT WIDGET ---

    const chatPopup = document.getElementById('chat-popup');
    const chatToggleBtn = document.getElementById('chat-toggle-btn');
    const closeBtn = document.getElementById('close-btn');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    if (chatToggleBtn) {
        chatToggleBtn.addEventListener('click', () => {
            chatPopup.classList.toggle('active');
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            chatPopup.classList.remove('active');
        });
    }

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userMessage = userInput.value.trim();
            if (!userMessage) return;

            addMessage(userMessage, 'user');
            userInput.value = '';
            const loadingMessage = addMessage('Coach FitCare sedang mengetik...', 'bot-loading');

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: userMessage })
                });
                const data = await response.json();
                loadingMessage.remove();

                if (data.answer) {
                    addMessage(data.answer, 'bot');
                } else {
                    addMessage('Maaf, terjadi kesalahan. Coba lagi nanti.', 'bot');
                }
            } catch (error) {
                loadingMessage.remove();
                addMessage('Tidak bisa terhubung ke server. Pastikan server berjalan.', 'bot');
                console.error("Error:", error);
            }
        });
    }

    function addMessage(text, type) {
        if (!chatMessages) return;
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', type);
        messageElement.textContent = text;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageElement;
    }
    
    // --- LOGIKA UNTUK TOMBOL CTA DI HOMEPAGE ---
    const mainCtaButton = document.querySelector('.chat-toggle-btn-main');
    
    if (mainCtaButton) {
        mainCtaButton.addEventListener('click', () => {
            if (chatToggleBtn) {
                chatToggleBtn.click();
            }
        });
    }

    // --- LOGIKA UNTUK FILTER DI HALAMAN WORKOUTS ---
    const searchInput = document.getElementById('search-input');
    const bodypartFilter = document.getElementById('bodypart-filter');
    const levelFilter = document.getElementById('level-filter');
    const workoutCards = document.querySelectorAll('.workout-card');

    function filterWorkouts() {
        if (workoutCards.length === 0) return; // Keluar jika tidak di Halaman Workouts
        
        const searchTerm = searchInput.value.toLowerCase();
        const bodypartTerm = bodypartFilter.value;
        const levelTerm = levelFilter.value;

        workoutCards.forEach(card => {
            const title = card.dataset.title || '';
            const bodypart = card.dataset.bodypart || '';
            const level = card.dataset.level || '';

            const titleMatch = title.includes(searchTerm);
            const bodypartMatch = (bodypartTerm === 'all' || bodypart === bodypartTerm);
            const levelMatch = (levelTerm === 'all' || level === levelTerm);

            if (titleMatch && bodypartMatch && levelMatch) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('keyup', filterWorkouts);
        bodypartFilter.addEventListener('change', filterWorkouts);
        levelFilter.addEventListener('change', filterWorkouts);
    }
});


// --- LOGIKA UNTUK FILTER DI HALAMAN NUTRITION ---
    const foodSearchInput = document.getElementById('food-search-input');
    const categoryFilter = document.getElementById('category-filter');
    const foodCards = document.querySelectorAll('.food-card');

    function filterFoods() {
        if (foodCards.length === 0) return; // Keluar jika tidak di Halaman Nutrition

        const searchTerm = foodSearchInput.value.toLowerCase();
        const categoryTerm = categoryFilter.value;

        foodCards.forEach(card => {
            const name = card.dataset.name || '';
            const category = card.dataset.category || '';

            const nameMatch = name.includes(searchTerm);
            const categoryMatch = (categoryTerm === 'all' || category === categoryTerm);

            if (nameMatch && categoryMatch) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    }

    if (foodSearchInput) {
        foodSearchInput.addEventListener('keyup', filterFoods);
        categoryFilter.addEventListener('change', filterFoods);
    }