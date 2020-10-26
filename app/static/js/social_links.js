$(window).on("load", () => {
	$(".social-del").click(toggleSocialInputDelete);
	$(".social-add").click(e => {
		e.preventDefault();
		
		const form_index = $(`#id_${FORM_PREFIX}-TOTAL_FORMS`).val();
		const new_form = $($("#social_form_empty").html().replace(/__prefix__/g, form_index));
		$(".social-inputs").append(new_form);
		$(`#id_${FORM_PREFIX}-TOTAL_FORMS`).val((form_index/1)+1);
		new_form.children(".social-del").click(toggleSocialInputDelete);
	});


	// enable after the click handler has been added
	$(".social-add, .social-del").prop("disabled", false);
});

const CLOSE = "delete";
const OPEN = "time-restore-setting";

function toggleSocialInputDelete(e) {
	e.preventDefault();

	if (parseInt($(this).attr("data-id").split("-")[1]) >= parseInt($(`#id_${FORM_PREFIX}-INITIAL_FORMS`).val())) {
		$(this).parent().remove();
		$(`#id_${FORM_PREFIX}-TOTAL_FORMS`).val(parseInt($(`#id_${FORM_PREFIX}-TOTAL_FORMS`).val())-1);
		return;
	}

	$(this).parent().children().filter(function() {
		return this.classList.length === 0 || !this.classList.contains("social-del")
	}).each((ind,elm) => $(elm).toggleClass("disabled"));

	const checkbox = $('#'+$(this).attr("data-id"))[0];
	checkbox.checked = !checkbox.checked;
	$(this).html(`<i class="zmdi zmdi-${$(this).html().includes(CLOSE) ? OPEN : CLOSE}" aria-hidden="true"></i>`);
}
