/**
 * Dedicated script for Hero Section & Vertical Scroll Animations
 */
(function () {
    function initHeroAnimations() {
        const videoSections = document.querySelectorAll('.js-video-section');

        const observerOptions = {
            threshold: 0.1
        };

        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-playing');
                    const playBtn = entry.target.querySelector('.btn-play');
                    if (playBtn) playBtn.classList.add('is-playing');
                }
            });
        }, observerOptions);

        videoSections.forEach(section => {
            animationObserver.observe(section);
            // Force play if already in view
            const rect = section.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                section.classList.add('is-playing');
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeroAnimations);
    } else {
        initHeroAnimations();
    }
})();
