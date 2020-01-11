let prevShownForm = null;

function init_comment(com) {
    let answer_button = com.querySelector('.answer_comment');
    let form = com.querySelector('.comment_form');

    answer_button.addEventListener('click', () => {
        if (prevShownForm != null)
            prevShownForm.style.display = 'none';
        form.style.display = 'inline';
        prevShownForm = form;
    });
}

document.querySelectorAll('.comment').forEach(init_comment);
