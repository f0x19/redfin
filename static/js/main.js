// API Base URL
const API_URL = '/api';

// State
let currentFilters = {};
let allProperties = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadProperties();
    initializeEventListeners();
});

// Event Listeners
function initializeEventListeners() {
    // Search input enter key
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchProperties();
            }
        });
    }
}

// Toggle Filters Panel
function toggleFilters() {
    const filtersPanel = document.getElementById('filtersPanel');
    filtersPanel.classList.toggle('active');
}

// Load Properties
async function loadProperties(filters = {}) {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const propertiesGrid = document.getElementById('propertiesGrid');
    const noResults = document.getElementById('noResults');
    const resultsCount = document.getElementById('resultsCount');
    
    // Show loading
    loadingSpinner.style.display = 'block';
    propertiesGrid.style.display = 'none';
    noResults.style.display = 'none';
    
    try {
        // Build query string
        const queryParams = new URLSearchParams();
        for (const [key, value] of Object.entries(filters)) {
            if (value) {
                queryParams.append(key, value);
            }
        }
        
        const response = await fetch(`${API_URL}/properties?${queryParams}`);
        const properties = await response.json();
        
        allProperties = properties;
        
        // Hide loading
        loadingSpinner.style.display = 'none';
        
        if (properties.length === 0) {
            noResults.style.display = 'block';
            resultsCount.textContent = '';
        } else {
            propertiesGrid.style.display = 'grid';
            resultsCount.textContent = `${properties.length} properties found`;
            renderProperties(properties);
        }
    } catch (error) {
        console.error('Error loading properties:', error);
        loadingSpinner.innerHTML = '<p>Error loading properties. Please try again.</p>';
    }
}

// Render Properties
function renderProperties(properties) {
    const propertiesGrid = document.getElementById('propertiesGrid');
    propertiesGrid.innerHTML = '';
    
    properties.forEach(property => {
        const card = createPropertyCard(property);
        propertiesGrid.appendChild(card);
    });
}

// Create Property Card
function createPropertyCard(property) {
    const card = document.createElement('div');
    card.className = 'property-card';
    card.onclick = () => viewProperty(property.id);
    
    card.innerHTML = `
        <div class="property-image">
            <img src="${property.image_url || 'https://via.placeholder.com/400x300?text=No+Image'}" 
                 alt="${property.title}"
                 onerror="this.src='https://via.placeholder.com/400x300?text=No+Image'">
            <button class="favorite-btn" onclick="toggleFavorite(event, ${property.id})">
                <i class="far fa-heart"></i>
            </button>
            <div class="property-status">${property.status}</div>
        </div>
        <div class="property-content">
            <div class="property-price">$${formatPrice(property.price)}</div>
            <h3 class="property-title">${property.title}</h3>
            <p class="property-address">
                <i class="fas fa-map-marker-alt"></i>
                ${property.address}, ${property.city}, ${property.state}
            </p>
            <div class="property-details">
                <div class="property-detail">
                    <i class="fas fa-bed"></i>
                    <span>${property.bedrooms} bd</span>
                </div>
                <div class="property-detail">
                    <i class="fas fa-bath"></i>
                    <span>${property.bathrooms} ba</span>
                </div>
                <div class="property-detail">
                    <i class="fas fa-ruler-combined"></i>
                    <span>${formatNumber(property.square_feet)} sqft</span>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Search Properties
function searchProperties() {
    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.trim();
    
    currentFilters.search = searchTerm;
    loadProperties(currentFilters);
}

// Apply Filters
function applyFilters() {
    const filters = {
        min_price: document.getElementById('minPrice').value,
        max_price: document.getElementById('maxPrice').value,
        bedrooms: document.getElementById('bedrooms').value,
        bathrooms: document.getElementById('bathrooms').value,
        property_type: document.getElementById('propertyType').value,
        city: document.getElementById('cityFilter').value,
        search: document.getElementById('searchInput').value
    };
    
    // Remove empty filters
    currentFilters = {};
    for (const [key, value] of Object.entries(filters)) {
        if (value) {
            currentFilters[key] = value;
        }
    }
    
    loadProperties(currentFilters);
}

// Clear Filters
function clearFilters() {
    // Reset all filter inputs
    document.getElementById('searchInput').value = '';
    document.getElementById('minPrice').value = '';
    document.getElementById('maxPrice').value = '';
    document.getElementById('bedrooms').value = '';
    document.getElementById('bathrooms').value = '';
    document.getElementById('propertyType').value = '';
    document.getElementById('cityFilter').value = '';
    
    currentFilters = {};
    loadProperties();
}

// View Property Detail
function viewProperty(propertyId) {
    window.location.href = `/property/${propertyId}`;
}

// Toggle Favorite
function toggleFavorite(event, propertyId) {
    event.stopPropagation(); // Prevent card click
    
    const button = event.currentTarget;
    const icon = button.querySelector('i');
    
    // Toggle favorite state
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        button.classList.add('active');
        
        // In a real app, save to backend
        saveFavorite(propertyId);
        
        showNotification('Added to favorites!');
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        button.classList.remove('active');
        
        // In a real app, remove from backend
        removeFavorite(propertyId);
        
        showNotification('Removed from favorites');
    }
}

// Save Favorite (placeholder for backend integration)
async function saveFavorite(propertyId) {
    try {
        const response = await fetch(`${API_URL}/favorites`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                property_id: propertyId,
                user_email: 'user@example.com' // In a real app, get from auth
            })
        });
        
        if (!response.ok) {
            console.error('Failed to save favorite');
        }
    } catch (error) {
        console.error('Error saving favorite:', error);
    }
}

// Remove Favorite (placeholder)
async function removeFavorite(propertyId) {
    // In a real app, call DELETE endpoint
    console.log('Removing favorite:', propertyId);
}

// Show Notification
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #48bb78;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
        style.remove();
    }, 3000);
}

// Utility Functions
function formatPrice(price) {
    return new Intl.NumberFormat('en-US').format(price);
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-US').format(num);
}

// Load favorites on page load (for navbar badge)
async function loadFavoritesCount() {
    try {
        const response = await fetch(`${API_URL}/favorites/user@example.com`);
        const favorites = await response.json();
        
        const favoritesLink = document.getElementById('favoritesLink');
        if (favorites.length > 0) {
            favoritesLink.innerHTML = `
                <i class="fas fa-heart"></i> Favorites (${favorites.length})
            `;
        }
    } catch (error) {
        console.error('Error loading favorites:', error);
    }
}

// Initialize favorites count
loadFavoritesCount();
