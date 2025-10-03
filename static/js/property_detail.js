// API Base URL
const API_URL = '/api';

// Get property ID from URL
const propertyId = window.location.pathname.split('/').pop();

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadPropertyDetail();
});

// Load Property Detail
async function loadPropertyDetail() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const propertyDetail = document.getElementById('propertyDetail');
    
    try {
        const response = await fetch(`${API_URL}/properties/${propertyId}`);
        
        if (!response.ok) {
            throw new Error('Property not found');
        }
        
        const property = await response.json();
        
        // Hide loading, show content
        loadingSpinner.style.display = 'none';
        propertyDetail.style.display = 'block';
        
        // Render property details
        renderPropertyDetail(property);
        
    } catch (error) {
        console.error('Error loading property:', error);
        loadingSpinner.innerHTML = `
            <p style="color: #c82021;">Property not found or error loading details.</p>
            <a href="/" class="btn btn-primary" style="margin-top: 1rem;">Back to Search</a>
        `;
    }
}

// Render Property Detail
function renderPropertyDetail(property) {
    // Main image
    document.getElementById('mainImage').src = property.image_url || 'https://via.placeholder.com/800x500?text=No+Image';
    
    // Title and address
    document.getElementById('propertyTitle').textContent = property.title;
    document.getElementById('propertyAddress').textContent = 
        `${property.address}, ${property.city}, ${property.state} ${property.zip_code}`;
    
    // Price
    document.getElementById('propertyPrice').textContent = `$${formatPrice(property.price)}`;
    
    // Stats
    document.getElementById('bedrooms').textContent = property.bedrooms;
    document.getElementById('bathrooms').textContent = property.bathrooms;
    document.getElementById('squareFeet').textContent = formatNumber(property.square_feet);
    document.getElementById('propertyType').textContent = property.property_type;
    
    // Description
    document.getElementById('propertyDescription').textContent = property.description;
    
    // Property details
    document.getElementById('yearBuilt').textContent = property.year_built || 'N/A';
    document.getElementById('lotSize').textContent = property.lot_size ? 
        `${formatNumber(property.lot_size)} sq ft` : 'N/A';
    document.getElementById('propertyTypeDetail').textContent = property.property_type;
    document.getElementById('propertyStatus').textContent = property.status;
    
    // Set mortgage calculator home price
    document.getElementById('homePrice').value = property.price;
}

// Toggle Favorite
function toggleFavorite() {
    const button = document.querySelector('.favorite-btn-large');
    const icon = button.querySelector('i');
    
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        showNotification('Added to favorites!');
        
        // Save to backend
        saveFavorite(propertyId);
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        showNotification('Removed from favorites');
        
        // Remove from backend
        removeFavorite(propertyId);
    }
}

// Save Favorite
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

// Remove Favorite
async function removeFavorite(propertyId) {
    // In a real app, call DELETE endpoint
    console.log('Removing favorite:', propertyId);
}

// Submit Contact Form
function submitContactForm(event) {
    event.preventDefault();
    
    // In a real app, send to backend
    showNotification('Message sent! An agent will contact you soon.');
    event.target.reset();
}

// Calculate Mortgage
function calculateMortgage() {
    const homePrice = parseFloat(document.getElementById('homePrice').value);
    const downPaymentPercent = parseFloat(document.getElementById('downPayment').value);
    const interestRate = parseFloat(document.getElementById('interestRate').value);
    const loanTerm = parseInt(document.getElementById('loanTerm').value);
    
    if (!homePrice || !downPaymentPercent || !interestRate || !loanTerm) {
        showNotification('Please fill in all calculator fields', 'error');
        return;
    }
    
    // Calculate loan amount
    const downPayment = homePrice * (downPaymentPercent / 100);
    const loanAmount = homePrice - downPayment;
    
    // Calculate monthly payment
    const monthlyRate = (interestRate / 100) / 12;
    const numberOfPayments = loanTerm * 12;
    
    const monthlyPayment = loanAmount * 
        (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) / 
        (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
    
    // Display result
    const resultDiv = document.getElementById('mortgageResult');
    const paymentDiv = document.getElementById('monthlyPayment');
    
    resultDiv.style.display = 'block';
    paymentDiv.textContent = `$${formatPrice(Math.round(monthlyPayment))}/mo`;
}

// Show Notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    const bgColor = type === 'success' ? '#48bb78' : '#f56565';
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${bgColor};
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
