// Changes the value of `id_${FORM_PREFIX}-TOTAL_FORMS`, if a valid argument d (delta) is given,
// and returns said value
const total_forms_val = d => {
	if (d === undefined || isNaN(parseInt(d))) d = 0;
	const elm = $(`#id_${FORM_PREFIX}-TOTAL_FORMS`);
	return elm.val(parseInt(elm.val())+d).val();
} 

$(window).on("load", () => {
	$(".social-del").click(toggleSocialInputDelete);
	$(".social-add").click(e => {
		e.preventDefault();
		
		const new_form = $($("#social_form_empty").html().replace(/__prefix__/g, total_forms_val()));
		$(".social-inputs").append(new_form);
		total_forms_val(1);
		new_form.children(".social-del").click(toggleSocialInputDelete);
	});

	// A protection against those with especially fast fingers that can press buttons before the script loads
	$(".social-add, .social-del").prop("disabled", false);
});

function toggleSocialInputDelete(e) {
	e.preventDefault();

	if (parseInt($(this).attr("data-id").split("-")[1]) >= parseInt($(`#id_${FORM_PREFIX}-INITIAL_FORMS`).val())) {
		total_forms_val(-1);

		// Updates the next input elements' numeric indices to account for the removal
		$(this).parent().nextAll().children().each(function() {
			const prefix = $(this).attr("id") === undefined ? "data-" : "";
			const split_id = $(this).attr(prefix+"id").split("-");
			const split_name = $(this).prop("name").split("-");
			split_id[1] = split_name[1] = parseInt(split_id[1])-1;
			$(this).attr(prefix+"id",split_id.join("-"));
			$(this).prop("name",split_name.join("-"));
		});
		$(this).parent().remove();
		return;
	}

	$(this).siblings().each((ind,elm) => $(elm).toggleClass("disabled"));

	const checkbox = $('#'+$(this).attr("data-id"))[0];
	checkbox.checked = !checkbox.checked;
	$(this).children("i").toggleClass("fa-trash").toggleClass("fa-trash-restore")
}
