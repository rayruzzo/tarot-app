// Utility to get CSRF token from cookie
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

// Attach event listener to all 'Get Interpretation' buttons
document.addEventListener('DOMContentLoaded', function() {

    const readingData = JSON.parse(document.getElementById('reading-data').textContent);

	const btn = document.querySelector('.get-interpretation-btn');
	if (!btn) return;
	btn.addEventListener('click', function() {
		console.log('[interpretCall.js] Using readingData:', readingData);
		btn.disabled = true;
		btn.textContent = 'Loading...';
		fetch('/api/interpret/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({ reading: readingData })
		})
		.then(response => {
			console.log('[interpretCall.js] Fetch response:', response);
			return response.json();
		})
		.then(data => {
			console.log('[interpretCall.js] Response data:', data);
			const target = document.querySelector('.interpretation-result');
			if (data.interpretation) {
				if (target) {
					target.innerHTML = data.interpretation;
					btn.style.display = 'none';
				} else {
					alert(data.interpretation);
				}
			} else if (data.error) {
				alert(data.error);
			}
		})
		.catch(err => {
			alert('Error: ' + err);
			console.error('[interpretCall.js] Fetch error:', err);
		})
		.finally(() => {
			btn.disabled = false;
			btn.textContent = 'Get Interpretation';
		});
	});
});
