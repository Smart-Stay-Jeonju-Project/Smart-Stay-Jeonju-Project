// 검색타입이 주소면 보여주고 아니면 안보여주는

function toggleSearchTermInput() {
    const searchType = document.getElementById('search_type').value;
    const textInputDiv = document.getElementById('text_input_div');
    const addressSelectDiv = document.getElementById('address_select_div');
    const textInput = document.getElementById('search_term');
    const addressSelect = document.getElementById('address_select');

    if (searchType === 'address') {
        textInputDiv.style.display = 'none';
        textInput.disabled = true;

        addressSelectDiv.style.display = 'block';
        addressSelect.disabled = false;
    } else {
        textInputDiv.style.display = 'block';
        textInput.disabled = false;

        addressSelectDiv.style.display = 'none';
        addressSelect.disabled = true;
    }
}

window.addEventListener('DOMContentLoaded', () => {
    toggleSearchTermInput();
});
