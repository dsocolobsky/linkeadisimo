console.log('ohaio');

let prevShownForm = null;
function init_comment(com) {
    let answer_button = com.querySelector('.answer_comment');
    let form = com.querySelector('.comment_form');

    answer_button.addEventListener('click', () => {
        if (prevShownForm != null)
            prevShownForm.style.display = 'none';
        form.style.display = 'flex';
        prevShownForm = form;
    });
}

function init_publications(pub) {
    let uparrow = pub.querySelector('.uparrow');

    uparrow.addEventListener('click', () => {
        console.log('Clicked ' + pub.id);

        axios({
            method: 'post',
            url: 'http://localhost:8000/upvote',
            headers: {
                "X-CSRFToken": csrftoken,
            },
            data: {
                id: pub.id,
            }
        }).then(data => location.reload())
            .catch(err => console.log(err))
    });
}

document.querySelectorAll('.comment').forEach(init_comment);

document.querySelectorAll('.publication').forEach(init_publications);
