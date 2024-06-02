odoo.define('ngo_select_city.form', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function () {
        $('#country').change(function () {
            var country_id = $(this).val();
            if (country_id) {
                ajax.jsonRpc('/get_states', 'call', {'country_id': parseInt(country_id)}).then(function (data) {
                    console.log(data)
                    var $state = $('#state');
                    $state.empty();
                    $state.append('<option value="">Şehir Seçiniz</option>');
                    $.each(data, function (index, state) {
                        $state.append($('<option>', {
                            value: state.id,
                            text: state.name
                        }));
                    });
                });
            } else {
                $('#state').empty();
                $('#state').append('<option value="">Şehir Seçiniz</option>');
            }
        });
        $('#state').change(function () {
            var state_id = $(this).val();
            if (state_id) {
                ajax.jsonRpc('/get_branches', 'call', {'state_id': parseInt(state_id)}).then(function (data) {
                    console.log(data)
                    var $branch = $('#branch');
                    $branch.empty();
                    $branch.append('<option value="">Şube Seçiniz</option>');
                    $.each(data, function (index, branch) {
                        $branch.append($('<option>', {
                            value: branch.id,
                            text: branch.name
                        }));
                    });
                });
            } else {
                $('#branch').empty();
                $('#branch').append('<option value="">Şube Seçiniz</option>');
            }
        });

        $('#show_branch_info').click(function () {
            var branch_id = $('#branch').val();
            if (branch_id) {
                ajax.jsonRpc('/get_branch_info', 'call', {'branch_id': parseInt(branch_id)}).then(function (data) {
                    if (data.error) {
                        $('#branch_info').html('<p>Şube bulunamadı.</p>');
                    } else {
                        $('#branch_info').html(data);
                    }
                });
            } else {
                $('#branch_info').empty();
            }
        });
    });
});