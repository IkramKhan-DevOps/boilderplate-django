/**
 * Global Form Submission Handler
 * Prevents duplicate AJAX form submissions across all modals
 * Handles create, update, and delete operations
 */

(function() {
    'use strict';

    // Track forms currently being submitted
    const submittingForms = new Set();

    /**
     * Initialize form handlers once DOM is ready
     */
    function initFormHandlers() {
        // Remove any existing handlers to prevent duplicates
        $(document).off('click', '[id^="submit-button-"]');
        $(document).off('click', '[id^="submit-button-for"]');
        $(document).off('submit', 'form[id^="delete-form-"]');
        $(document).off('submit', 'form[id^="modal-form-"]');

        // Handle UPDATE form submissions
        $(document).on('click', '[id^="submit-button-"]', handleUpdateSubmit);

        // Handle CREATE form submissions
        $(document).on('click', '[id^="submit-button-for"]', handleCreateSubmit);

        // Handle DELETE form submissions
        $(document).on('submit', 'form[id^="delete-form-"]', handleDeleteSubmit);
    }

    /**
     * Handle UPDATE form submission
     */
    function handleUpdateSubmit(e) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        const $button = $(this);
        const buttonId = $button.attr('id');
        const instancePk = buttonId.replace('submit-button-', '');
        const formId = 'modal-form-' + instancePk;

        // Prevent duplicate submissions
        if (submittingForms.has(formId)) {
            console.log('Form already being submitted, ignoring...', formId);
            return false;
        }

        const $form = $('#' + formId);
        if ($form.length === 0) {
            console.error('Form not found:', formId);
            return false;
        }

        submitForm($form, $button, formId);
        return false;
    }

    /**
     * Handle CREATE form submission
     */
    function handleCreateSubmit(e) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        const $button = $(this);
        const buttonId = $button.attr('id');
        const modelName = buttonId.replace('submit-button-for', '');
        const formId = 'modal-form-for' + modelName;

        // Prevent duplicate submissions
        if (submittingForms.has(formId)) {
            console.log('Form already being submitted, ignoring...', formId);
            return false;
        }

        const $form = $('#' + formId);
        if ($form.length === 0) {
            console.error('Form not found:', formId);
            return false;
        }

        submitForm($form, $button, formId);
        return false;
    }

    /**
     * Handle DELETE form submission
     */
    function handleDeleteSubmit(e) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        const $form = $(this);
        const formId = $form.attr('id');

        // Prevent duplicate submissions
        if (submittingForms.has(formId)) {
            console.log('Delete form already being submitted, ignoring...', formId);
            return false;
        }

        const $button = $form.find('button[type="submit"]');
        submitDeleteForm($form, $button, formId);
        return false;
    }

    /**
     * Submit a form via AJAX (for create/update)
     */
    function submitForm($form, $button, formId) {
        // Mark as submitting
        submittingForms.add(formId);

        // Disable button and show spinner
        const originalText = $button.html();
        $button.prop('disabled', true)
               .html('<span class="spinner-border spinner-border-sm me-2"></span>Saving...');

        const url = $form.attr('action');
        const formData = new FormData($form[0]);
        const $modal = $form.closest('.modal');

        // Clear previous errors
        clearFieldErrors($form);
        clearGeneralError($modal);

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            dataType: 'json',
            processData: false,
            contentType: false,
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                submittingForms.delete(formId);
                $button.prop('disabled', false).html(originalText);

                if (response.status === "error") {
                    if (response.error_list && Object.keys(response.error_list).length > 0) {
                        showFieldErrors($form, response.error_list);
                    } else {
                        showGeneralError($modal, response.message || 'Form validation failed.');
                    }
                } else {
                    $modal.modal('hide');
                    if (typeof toast_message === 'function') {
                        toast_message(response.message || "Saved successfully!", "success");
                    }

                    setTimeout(function() {
                        if (response.redirect_url) {
                            window.location.href = response.redirect_url;
                        } else {
                            location.reload();
                        }
                    }, 500);
                }
            },
            error: function(xhr, status, error) {
                submittingForms.delete(formId);
                $button.prop('disabled', false).html(originalText);

                console.error('AJAX Error:', error);
                const resp = xhr.responseJSON;
                if (resp && resp.error_list) {
                    showFieldErrors($form, resp.error_list);
                } else if (resp && resp.message) {
                    showGeneralError($modal, resp.message);
                } else {
                    showGeneralError($modal, 'Unexpected server error. Please try again.');
                }
            }
        });
    }

    /**
     * Submit a delete form via AJAX
     */
    function submitDeleteForm($form, $button, formId) {
        // Mark as submitting
        submittingForms.add(formId);

        // Disable button and show spinner
        const originalText = $button.html();
        $button.prop('disabled', true)
               .html('<span class="spinner-border spinner-border-sm me-2"></span>Deleting...');

        $.ajax({
            url: $form.attr('action'),
            type: 'POST',
            data: $form.serialize(),
            success: function(response, textStatus, xhr) {
                submittingForms.delete(formId);

                // Close the modal
                const $modal = $form.closest('.modal');
                if ($modal.length) {
                    $modal.modal('hide');
                }

                // Check for redirect URL in the form action query params
                const actionUrl = $form.attr('action');
                const urlParams = new URLSearchParams(actionUrl.split('?')[1] || '');
                const redirectUrl = urlParams.get('redirect_url');

                if (redirectUrl) {
                    // Convert Django URL name to actual URL path
                    // Format: app_name:view_name -> /app_name/
                    const parts = redirectUrl.split(':');
                    if (parts.length === 2) {
                        window.location.href = '/' + parts[0] + '/';
                    } else {
                        window.location.href = '/' + redirectUrl.replace(/:/g, '/') + '/';
                    }
                } else if (response && response.redirect_url) {
                    window.location.href = response.redirect_url;
                } else {
                    // Fallback: go to referrer or home
                    window.location.href = document.referrer || '/';
                }
            },
            error: function(xhr) {
                submittingForms.delete(formId);
                $button.prop('disabled', false).html(originalText);

                const resp = xhr.responseJSON;
                if (resp && resp.message) {
                    alert('Error: ' + resp.message);
                } else {
                    alert('An error occurred while deleting. Please try again.');
                }
            }
        });
    }

    /**
     * Clear field-level error styling
     */
    function clearFieldErrors($form) {
        $form.find('.is-invalid').removeClass('is-invalid');
        $form.find('.invalid-feedback').remove();
    }

    /**
     * Clear general error messages
     */
    function clearGeneralError($modal) {
        $modal.find('.modal-errors').hide().empty();
    }

    /**
     * Show field-level validation errors
     */
    function showFieldErrors($form, errorList) {
        let generalErrors = [];

        $.each(errorList, function(fieldName, messages) {
            if (fieldName === "__all__") {
                messages.forEach(function(msgObj) {
                    generalErrors.push(msgObj.message);
                });
            } else {
                const fieldId = 'id_' + fieldName;
                const $field = $form.find('#' + fieldId);
                if ($field.length > 0) {
                    $field.addClass('is-invalid');
                    const $feedback = $('<div>', {class: 'invalid-feedback'});
                    $feedback.text(messages[0].message);
                    if ($field.next('.invalid-feedback').length === 0) {
                        $field.after($feedback);
                    }
                }
            }
        });

        if (generalErrors.length > 0) {
            const $modal = $form.closest('.modal');
            showGeneralError($modal, generalErrors.join('<br>'));
        }
    }

    /**
     * Show general error message
     */
    function showGeneralError($modal, message) {
        const $errors = $modal.find('.modal-errors');
        if ($errors.length > 0) {
            $errors.html('<div>' + message + '</div>').show();
        } else {
            // Fallback if .modal-errors doesn't exist
            const $modalBody = $modal.find('.modal-body');
            $modalBody.prepend('<div class="alert alert-danger modal-errors">' + message + '</div>');
        }
    }

    // Initialize when document is ready
    $(document).ready(function() {
        initFormHandlers();
        console.log('Global form handlers initialized');
    });

    // Re-initialize after AJAX loads (for dynamically loaded modals)
    $(document).on('shown.bs.modal', '.modal', function() {
        initFormHandlers();
    });

})();