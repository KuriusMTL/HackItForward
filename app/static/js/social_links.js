$(window).on('load', () => {
	$('.social-del').click(deleteSocialInput);

	$('.social-add').click(evt => {
		evt.preventDefault();
		
		const newSelect = $("<select></select>")
			.prop("name","social-type")
			.addClass("form-group-label")
			.addClass("btn-grey")
			.addClass("select");

		for (let type of SOCIAL_TYPES) {
			const opt = $("<option></option>")
				.val(type)
				.text(type);
			newSelect.append(opt);
		}

		const newInput = $("<input>")
			.addClass("form-group-input")
			.prop("type","text")
			.prop("name","social-content")
			.prop("placeholder",HELP_TEXT)
			.prop("required",true);

		const newBtn = $("<button></button>")
			.addClass("form-group-btn")
			.addClass("social-del")
			.text("x")
			.click(deleteSocialInput);

		const newField = $("<div></div>")
			.addClass("form-group")
	    	.append(newSelect, newInput, newBtn);

		$('.social-inputs').append(newField);
	});

	// enable after the click handler has been added
	$('.social-add').prop("disabled",false);
	$('.social-del').prop("disabled",false);
});

function deleteSocialInput(evt) {
	evt.preventDefault();
	$(this).parent().remove();
}
