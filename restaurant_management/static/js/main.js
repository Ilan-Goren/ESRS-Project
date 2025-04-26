/**
 * Restaurant Management System
 * Main JavaScript File
 */

// Wait for document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Handle sidebar toggle
    setupSidebarToggle();
    
    // Make tables sortable if data-sortable attribute is present
    setupSortableTables();
    
    // Handle confirmation modals
    setupConfirmationModals();
    
    // Initialize auto-dismissing alerts
    setupAutoDismissAlerts();
    
    // Handle low stock and expiry date highlighting
    highlightInventoryStatus();
    
    // Setup dynamic form elements
    setupDynamicForms();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Setup sidebar toggle for mobile view
 */
function setupSidebarToggle() {
    const sidebarToggleBtn = document.querySelector('.navbar-toggler');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Close sidebar when clicking outside of it
        document.addEventListener('click', function(event) {
            if (!sidebar.contains(event.target) && !sidebarToggleBtn.contains(event.target)) {
                if (sidebar.classList.contains('show')) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }
}

/**
 * Make tables sortable
 */
function setupSortableTables() {
    const sortableTables = document.querySelectorAll('table[data-sortable="true"]');
    
    sortableTables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sortable="true"]');
        
        headers.forEach(header => {
            header.classList.add('cursor-pointer');
            
            // Add sort icon
            const sortIcon = document.createElement('i');
            sortIcon.classList.add('fas', 'fa-sort', 'ms-1', 'opacity-50');
            header.appendChild(sortIcon);
            
            header.addEventListener('click', () => {
                const columnIndex = Array.from(header.parentNode.children).indexOf(header);
                const isAscending = header.getAttribute('data-sort-direction') !== 'asc';
                
                // Reset all headers
                headers.forEach(h => {
                    h.setAttribute('data-sort-direction', '');
                    const icon = h.querySelector('i');
                    if (icon) {
                        icon.className = 'fas fa-sort ms-1 opacity-50';
                    }
                });
                
                // Set current header
                header.setAttribute('data-sort-direction', isAscending ? 'asc' : 'desc');
                const currentIcon = header.querySelector('i');
                if (currentIcon) {
                    currentIcon.className = `fas fa-sort-${isAscending ? 'up' : 'down'} ms-1`;
                    currentIcon.classList.remove('opacity-50');
                }
                
                // Sort the table
                sortTable(table, columnIndex, isAscending);
            });
        });
    });
}

/**
 * Sort table by column
 * 
 * @param {HTMLElement} table - The table to sort
 * @param {number} columnIndex - Index of the column to sort by
 * @param {boolean} ascending - Sort direction (true for ascending)
 */
function sortTable(table, columnIndex, ascending) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Sort the rows
    const sortedRows = rows.sort((rowA, rowB) => {
        const cellA = rowA.querySelectorAll('td')[columnIndex]?.textContent.trim() || '';
        const cellB = rowB.querySelectorAll('td')[columnIndex]?.textContent.trim() || '';
        
        // Check if the cells contain numbers
        const numA = parseFloat(cellA);
        const numB = parseFloat(cellB);
        
        if (!isNaN(numA) && !isNaN(numB)) {
            return ascending ? numA - numB : numB - numA;
        }
        
        // Otherwise, compare as strings
        return ascending
            ? cellA.localeCompare(cellB)
            : cellB.localeCompare(cellA);
    });
    
    // Clear the tbody and append the sorted rows
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }
    
    sortedRows.forEach(row => {
        tbody.appendChild(row);
    });
}

/**
 * Setup confirmation modals for delete/critical actions
 */
function setupConfirmationModals() {
    const confirmButtons = document.querySelectorAll('[data-confirm="true"]');
    
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const message = button.getAttribute('data-confirm-message') || 'Are you sure you want to perform this action?';
            const title = button.getAttribute('data-confirm-title') || 'Confirm Action';
            const confirmText = button.getAttribute('data-confirm-text') || 'Confirm';
            const cancelText = button.getAttribute('data-confirm-cancel') || 'Cancel';
            const confirmClass = button.getAttribute('data-confirm-class') || 'btn-danger';
            
            // Create the modal dynamically
            const modalId = 'confirmModal' + Math.floor(Math.random() * 1000);
            const modalHtml = `
                <div class="modal fade" id="${modalId}" tabindex="-1" aria-labelledby="${modalId}Label" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="${modalId}Label">${title}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                ${message}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">${cancelText}</button>
                                <button type="button" class="btn ${confirmClass}" id="${modalId}-confirm">${confirmText}</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add the modal to the body
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            
            // Create and show the modal
            const modalEl = document.getElementById(modalId);
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
            
            // Handle confirm button click
            document.getElementById(`${modalId}-confirm`).addEventListener('click', function() {
                // Close the modal
                modal.hide();
                
                // Execute the original action
                if (button.tagName === 'A') {
                    window.location.href = button.getAttribute('href');
                } else if (button.form) {
                    button.form.submit();
                }
                
                // Remove the modal after closing
                modalEl.addEventListener('hidden.bs.modal', function() {
                    modalEl.remove();
                });
            });
            
            // Remove the modal when hidden
            modalEl.addEventListener('hidden.bs.modal', function() {
                modalEl.remove();
            });
        });
    });
}

/**
 * Setup auto-dismissing alerts after a timeout
 */
function setupAutoDismissAlerts() {
    const autoAlerts = document.querySelectorAll('.alert-dismissible[data-auto-dismiss="true"]');
    
    autoAlerts.forEach(alert => {
        const timeout = parseInt(alert.getAttribute('data-dismiss-timeout')) || 5000;
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, timeout);
    });
}

/**
 * Highlight inventory items with low stock or nearing expiry
 */
function highlightInventoryStatus() {
    const inventoryCards = document.querySelectorAll('.inventory-card');
    
    inventoryCards.forEach(card => {
        // Check for low stock
        const quantity = parseInt(card.getAttribute('data-quantity')) || 0;
        const reorderLevel = parseInt(card.getAttribute('data-reorder-level')) || 0;
        
        if (quantity <= reorderLevel) {
            card.classList.add('low-stock');
            
            // Add a badge if it doesn't exist
            if (!card.querySelector('.badge-low-stock')) {
                const badge = document.createElement('span');
                badge.className = 'badge bg-warning badge-low-stock position-absolute top-0 end-0 m-2';
                badge.textContent = 'Low Stock';
                card.appendChild(badge);
            }
        }
        
        // Check for expiry
        const expiryDate = card.getAttribute('data-expiry-date');
        if (expiryDate) {
            const expiry = new Date(expiryDate);
            const today = new Date();
            const daysUntilExpiry = Math.floor((expiry - today) / (1000 * 60 * 60 * 24));
            
            if (daysUntilExpiry < 0) {
                card.classList.add('expired');
                
                // Add a badge if it doesn't exist
                if (!card.querySelector('.badge-expired')) {
                    const badge = document.createElement('span');
                    badge.className = 'badge bg-danger badge-expired position-absolute top-0 end-0 m-2';
                    badge.textContent = 'Expired';
                    card.appendChild(badge);
                }
            } else if (daysUntilExpiry < 7) {
                card.classList.add('expiring-soon');
                
                // Add a badge if it doesn't exist
                if (!card.querySelector('.badge-expiring')) {
                    const badge = document.createElement('span');
                    badge.className = 'badge bg-warning badge-expiring position-absolute top-0 end-0 m-2';
                    badge.textContent = `Expires in ${daysUntilExpiry} days`;
                    card.appendChild(badge);
                }
            }
        }
    });
}

/**
 * Setup dynamic form elements (like add more fields, etc)
 */
function setupDynamicForms() {
    // Handle "Add more items" functionality for order items
    const addItemBtn = document.querySelector('.add-more-items');
    
    if (addItemBtn) {
        addItemBtn.addEventListener('click', function() {
            const itemsContainer = document.getElementById('order-items-container');
            const itemTemplate = document.getElementById('item-template');
            
            if (itemsContainer && itemTemplate) {
                const newItem = itemTemplate.content.cloneNode(true);
                const itemCount = itemsContainer.children.length;
                
                // Update IDs and names for the new item
                newItem.querySelectorAll('[name], [id], [for]').forEach(el => {
                    if (el.hasAttribute('name')) {
                        el.setAttribute('name', el.getAttribute('name').replace('__prefix__', itemCount));
                    }
                    if (el.hasAttribute('id')) {
                        el.setAttribute('id', el.getAttribute('id').replace('__prefix__', itemCount));
                    }
                    if (el.hasAttribute('for')) {
                        el.setAttribute('for', el.getAttribute('for').replace('__prefix__', itemCount));
                    }
                });
                
                // Add the new item to the container
                itemsContainer.appendChild(newItem);
                
                // Add a remove button to the new item
                const newItemDiv = itemsContainer.lastElementChild;
                const removeBtn = document.createElement('button');
                removeBtn.type = 'button';
                removeBtn.className = 'btn btn-outline-danger remove-item mt-2';
                removeBtn.innerHTML = '<i class="fas fa-trash"></i> Remove';
                removeBtn.addEventListener('click', function() {
                    newItemDiv.remove();
                });
                
                newItemDiv.appendChild(removeBtn);
            }
        });
    }
    
    // Handle supplier/category dependent fields
    setupDependentFields();
}

/**
 * Setup dependent form fields (e.g., when selecting a supplier, load related items)
 */
function setupDependentFields() {
    const dependentSelects = document.querySelectorAll('select[data-depends-on]');
    
    dependentSelects.forEach(select => {
        const dependsOn = document.getElementById(select.getAttribute('data-depends-on'));
        
        if (dependsOn) {
            // Store the original options
            const originalOptions = Array.from(select.options);
            
            // Function to filter options based on the parent select
            const filterOptions = () => {
                const selectedValue = dependsOn.value;
                
                // Clear current options
                select.innerHTML = '';
                
                // Add default option
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = `Select ${select.getAttribute('data-entity') || 'item'}`;
                select.appendChild(defaultOption);
                
                // Filter and add relevant options
                originalOptions.forEach(option => {
                    if (option.value === '' || option.getAttribute('data-parent') === selectedValue) {
                        select.appendChild(option.cloneNode(true));
                    }
                });
                
                // Trigger change event
                select.dispatchEvent(new Event('change'));
            };
            
            // Initial filter
            filterOptions();
            
            // Filter on parent change
            dependsOn.addEventListener('change', filterOptions);
        }
    });
}