console.log('ohaio');

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

function init_publications(pub) {
    let uparrow = pub.querySelector('.uparrow');

    uparrow.addEventListener('click', () => {
        console.log('Clicked ' + pub.id);
    });
}

document.querySelectorAll('.comment').forEach(init_comment);

document.querySelectorAll('.publication').forEach(init_publications);
