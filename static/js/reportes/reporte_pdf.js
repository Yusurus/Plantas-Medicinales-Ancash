document.getElementById('plantSearch').addEventListener('keyup', function() {
    let filter = this.value.toLowerCase();
    let plantCards = document.querySelectorAll('.plant-card');

    plantCards.forEach(function(card) {
        let plantName = card.getAttribute('data-plant-name');
        if (plantName.includes(filter)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
});