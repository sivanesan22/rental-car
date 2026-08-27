document.addEventListener('DOMContentLoaded', () => {
    // 1. Sticky Navbar on Scroll
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // 2. Mobile Nav Toggle
    const mobileToggle = document.getElementById('mobile-toggle');
    const navLinks = document.getElementById('nav-links');
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = mobileToggle.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.className = 'fa-solid fa-xmark';
            } else {
                icon.className = 'fa-solid fa-bars';
            }
        });
    }

    // 3. Auto-Dismiss Alert Messages
    const messages = document.getElementById('messages-container');
    if (messages) {
        setTimeout(() => {
            messages.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
            messages.style.opacity = '0';
            messages.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                messages.remove();
            }, 500);
        }, 5000);
    }

    // 4. Booking Real-Time Cost Calculator
    const startDateInput = document.getElementById('booking-start-date');
    const endDateInput = document.getElementById('booking-end-date');
    const priceSummary = document.getElementById('price-summary');
    const submitBtn = document.getElementById('submit-booking-btn');

    if (startDateInput && endDateInput && priceSummary) {
        // Set minimum booking start date to today
        const today = new Date().toISOString().split('T')[0];
        startDateInput.setAttribute('min', today);
        endDateInput.setAttribute('min', today);

        const dailyRate = parseFloat(document.getElementById('car-daily-rate').dataset.rate);
        
        const calculateCost = () => {
            const startVal = startDateInput.value;
            const endVal = endDateInput.value;
            
            if (startVal && endVal) {
                const start = new Date(startVal);
                const end = new Date(endVal);
                
                // Keep end date field at minimum the start date
                endDateInput.setAttribute('min', startVal);

                if (end >= start) {
                    const diffTime = Math.abs(end - start);
                    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                    const days = diffDays === 0 ? 1 : diffDays; // Minimum 1 day rate
                    
                    const subtotal = dailyRate * days;
                    const fee = parseFloat((subtotal * 0.05).toFixed(2)); // 5% service fee
                    const total = subtotal + fee;

                    // Update UI elements
                    document.getElementById('summary-days').innerText = days;
                    document.getElementById('summary-subtotal').innerText = `$${subtotal.toFixed(2)}`;
                    document.getElementById('summary-fee').innerText = `$${fee.toFixed(2)}`;
                    document.getElementById('summary-total').innerText = `$${total.toFixed(2)}`;
                    
                    priceSummary.style.display = 'block';
                    if (submitBtn) submitBtn.disabled = false;
                } else {
                    priceSummary.style.display = 'none';
                    if (submitBtn) submitBtn.disabled = true;
                }
            } else {
                priceSummary.style.display = 'none';
            }
        };

        startDateInput.addEventListener('change', () => {
            if (endDateInput.value && endDateInput.value < startDateInput.value) {
                endDateInput.value = startDateInput.value;
            }
            calculateCost();
        });
        endDateInput.addEventListener('change', calculateCost);
    }
});
