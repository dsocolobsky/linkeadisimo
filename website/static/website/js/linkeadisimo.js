console.log('ohaio');

let prevShownForm = null;
function init_comment(com) {
    console.log("Initing comment " + com.id);

    let answer_button = com.querySelector('.answer_comment');
    let uparrow = com.querySelector('.uparrow');
    let form = com.querySelector('.comment_form');

    if (answer_button != null) {
        answer_button.addEventListener('click', () => {
            if (prevShownForm != null)
                prevShownForm.style.display = 'none';
            form.style.display = 'flex';
            prevShownForm = form;
        });
    }

    if (uparrow != null) {
        uparrow.addEventListener('click', () => {
            console.log("Voting for " + com.id);
            axios({
                method: 'post',
                url: 'http://localhost:8000/upvote_comment',
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                data: {
                    id: com.id,
                }
            }).then(data => {
                console.log("Voted " + com.id);
                location.reload()
            })
                .catch(err => console.log(err))
        });
    }
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
