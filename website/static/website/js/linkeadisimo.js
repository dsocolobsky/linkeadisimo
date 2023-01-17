console.log('linkeadisimo.js initializating');

let prevShownForm = null;
function init_comment(com) {
    let answer_button = com.querySelector('.answer_comment');
    let form = com.querySelector('.comment_form');

    if (answer_button != null) {
        answer_button.addEventListener('click', () => {
            if (prevShownForm != null)
                prevShownForm.style.display = 'none';
            form.style.display = 'flex';
            prevShownForm = form;
        });
    }
}

document.querySelectorAll('.comment').forEach(init_comment);

// HTMX by default will not swap on any errors, allow swapping on 422 for form errors
document.body.addEventListener('htmx:beforeOnLoad', function (evt) {
    if (evt.detail.xhr.status === 422) {
        evt.detail.shouldSwap = true;
        evt.detail.isError = false;
    }
});