let currentProfile = null;
let startX = 0;
let currentX = 0;

// Update the base URL to match the backend
const BASE_URL = 'http://localhost:5000';

function showLoading() {
    const loading = document.createElement('div');
    loading.className = 'loading';
    document.querySelector('.card-container').appendChild(loading);
}

function hideLoading() {
    const loading = document.querySelector('.loading');
    if (loading) loading.remove();
}

function showMatch() {
    const matchOverlay = document.createElement('div');
    matchOverlay.className = 'match-animation';
    matchOverlay.innerHTML = `
        <div class="match-content">
            <h1>It's a Match! 🎉</h1>
            <p>You can now start chatting</p>
        </div>
    `;
    document.body.appendChild(matchOverlay);
    
    setTimeout(() => {
        matchOverlay.addEventListener('animationend', () => {
            matchOverlay.remove();
        });
        matchOverlay.style.animation = 'fadeOut 0.3s ease-out';
    }, 2000);
}

async function loadNewProfile() {
    showLoading();
    try {
        const response = await fetch(`${BASE_URL}/api/users/random`);
        currentProfile = await response.json();
        
        const card = document.getElementById('current-card');
        card.style.animation = 'slideIn 0.5s ease-out';
        
        document.getElementById('profile-pic').src = currentProfile.photos[0];
        document.getElementById('profile-name').textContent = currentProfile.name;
        document.getElementById('profile-age').textContent = currentProfile.age;
        document.getElementById('profile-bio').textContent = currentProfile.bio;
    } catch (error) {
        console.error('Error loading profile:', error);
    } finally {
        hideLoading();
    }
}

function handleSwipe(direction) {
    const card = document.getElementById('current-card');
    card.style.transition = 'transform 0.5s ease-out';
    card.style.transform = `translateX(${direction === 'right' ? '150%' : '-150%'}) rotate(${direction === 'right' ? '20deg' : '-20deg'})`;
    
    fetch('http://localhost:5000/api/swipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            swiper_id: 'current-user-id',
            swiped_id: currentProfile.id,
            direction: direction
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.match) {
            showMatch();
        }
        setTimeout(() => {
            card.style.transition = 'none';
            card.style.transform = 'translateX(0) rotate(0)';
            loadNewProfile();
        }, 500);
    });
}

// Touch events for mobile swiping
let touchStartX = 0;
let touchMoveX = 0;

document.getElementById('current-card').addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
});

document.getElementById('current-card').addEventListener('touchmove', (e) => {
    touchMoveX = e.touches[0].clientX;
    const diff = touchMoveX - touchStartX;
    const card = document.getElementById('current-card');
    card.style.transform = `translateX(${diff}px) rotate(${diff * 0.1}deg)`;
});

document.getElementById('current-card').addEventListener('touchend', (e) => {
    const diff = touchMoveX - touchStartX;
    if (Math.abs(diff) > 100) {
        handleSwipe(diff > 0 ? 'right' : 'left');
    }
});

document.getElementById('like').addEventListener('click', () => handleSwipe('right'));
document.getElementById('dislike').addEventListener('click', () => handleSwipe('left'));

// Initialize
loadNewProfile(); 