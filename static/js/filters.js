// Product filtering and sorting functionality
class ProductFilters {
    constructor() {
        this.productsGrid = document.getElementById('productsGrid');
        this.products = Array.from(this.productsGrid.querySelectorAll('.product-card'));
        this.sortSelect = document.getElementById('sortSelect');
        this.priceMin = document.getElementById('priceMin');
        this.priceMax = document.getElementById('priceMax');
        this.availabilityFilter = document.getElementById('availabilityFilter');
        this.applyFiltersBtn = document.getElementById('applyFilters');
        this.resetFiltersBtn = document.getElementById('resetFilters');
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupPriceInputs();
    }
    
    setupEventListeners() {
        this.sortSelect.addEventListener('change', () => this.handleSorting());
        this.applyFiltersBtn.addEventListener('click', () => this.applyFilters());
        this.resetFiltersBtn.addEventListener('click', () => this.resetFilters());
        
        // Real-time filtering for price inputs
        this.priceMin.addEventListener('input', 
            this.debounce(() => this.applyFilters(), 300));
        this.priceMax.addEventListener('input', 
            this.debounce(() => this.applyFilters(), 300));
    }
    
    setupPriceInputs() {
        // Set min and max values based on product prices
        const prices = this.products.map(product => 
            parseInt(product.dataset.price) || 0
        );
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        
        this.priceMin.placeholder = minPrice;
        this.priceMax.placeholder = maxPrice;
    }
    
    handleSorting() {
        const sortValue = this.sortSelect.value;
        let sortedProducts;
        
        switch (sortValue) {
            case 'price-low':
                sortedProducts = this.sortByPrice('asc');
                break;
            case 'price-high':
                sortedProducts = this.sortByPrice('desc');
                break;
            case 'name':
                sortedProducts = this.sortByName();
                break;
            case 'newest':
            default:
                sortedProducts = this.sortByDate();
                break;
        }
        
        this.renderSortedProducts(sortedProducts);
    }
    
    sortByPrice(order = 'asc') {
        return [...this.products].sort((a, b) => {
            const priceA = parseInt(a.dataset.price) || 0;
            const priceB = parseInt(b.dataset.price) || 0;
            
            return order === 'asc' ? priceA - priceB : priceB - priceA;
        });
    }
    
    sortByName() {
        return [...this.products].sort((a, b) => {
            const nameA = a.querySelector('.product-name').textContent.toLowerCase();
            const nameB = b.querySelector('.product-name').textContent.toLowerCase();
            return nameA.localeCompare(nameB);
        });
    }
    
    sortByDate() {
        return [...this.products].sort((a, b) => {
            const dateA = new Date(a.dataset.date);
            const dateB = new Date(b.dataset.date);
            return dateB - dateA;
        });
    }
    
    applyFilters() {
        const minPrice = parseInt(this.priceMin.value) || 0;
        const maxPrice = parseInt(this.priceMax.value) || Infinity;
        const availability = this.availabilityFilter.value;
        
        const filteredProducts = this.products.filter(product => {
            const price = parseInt(product.dataset.price) || 0;
            const isNew = product.querySelector('.product-badge.new');
            const inStock = !product.querySelector('.out-of-stock-label');
            
            // Price filter
            if (price < minPrice || price > maxPrice) {
                return false;
            }
            
            // Availability filter
            if (availability === 'in-stock' && !inStock) {
                return false;
            }
            if (availability === 'new-arrivals' && !isNew) {
                return false;
            }
            
            return true;
        });
        
        this.renderFilteredProducts(filteredProducts);
        this.updateProductCount(filteredProducts.length);
    }
    
    resetFilters() {
        this.priceMin.value = '';
        this.priceMax.value = '';
        this.availabilityFilter.value = '';
        this.sortSelect.value = 'newest';
        
        this.renderFilteredProducts(this.products);
        this.updateProductCount(this.products.length);
    }
    
    renderSortedProducts(sortedProducts) {
        this.productsGrid.innerHTML = '';
        sortedProducts.forEach(product => {
            this.productsGrid.appendChild(product);
        });
    }
    
    renderFilteredProducts(filteredProducts) {
        this.productsGrid.innerHTML = '';
        
        if (filteredProducts.length === 0) {
            this.showNoResults();
            return;
        }
        
        filteredProducts.forEach(product => {
            this.productsGrid.appendChild(product);
        });
    }
    
    showNoResults() {
        const noResults = document.createElement('div');
        noResults.className = 'empty-state';
        noResults.innerHTML = `
            <h3>No products found</h3>
            <p>Try adjusting your filters or browse our complete collection</p>
            <button class="cta-button" onclick="productFilters.resetFilters()">Reset Filters</button>
        `;
        this.productsGrid.appendChild(noResults);
    }
    
    updateProductCount(count) {
        const countElement = document.querySelector('.products-count strong');
        if (countElement) {
            countElement.textContent = count;
        }
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize filters when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('productsGrid')) {
        window.productFilters = new ProductFilters();
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProductFilters;
}