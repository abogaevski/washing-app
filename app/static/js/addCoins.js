function addCoinsForPartner(csrf, item, balance, url) {

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': csrf,
            'item': item,
            'balance': balance
        },
        success: function(data) {
            $('td[data-col-id=partner_balance_' + data.partner + '] b').text(data.new_balance)
            $('#contractor-balance span').text(data.new_contractor_balance)
            $('#message-text span').text(data.message)
            $('input[data-item-balance]').val('')
            $('#message-text').removeClass('d-none').addClass(data.class)

            setTimeout(function(){
                $('#message-text').removeClass(data.class).addClass('d-none')
            }, 5000)
        }
    });

}