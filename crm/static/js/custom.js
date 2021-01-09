
    var myCarousel = document.querySelector('#noteCarousel')
    var carousel = new bootstrap.Carousel(myCarousel, {interval: false})

    document.querySelector('.carousel-control-prev').addEventListener('click', function () {
        carousel.prev()
    })

    document.querySelector('.carousel-control-next').addEventListener('click', function () {
        carousel.next()
    })

