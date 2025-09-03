<script setup>
</script>

<template>
    <!-- Pie de pagina -->
    <div class="row my-5 text-center">
        <div class="col">
            <h5 class="titulos">Redes sociales</h5>
            <p class="subtitulos">No te pierdas de nuestras noticias.</p>
        </div>
    </div>

    <div class="row my-4 justify-content-center g-3">
        <!-- Facebook -->
         <div class = "col-12 col-sm-6 col-md-4 col-lg-2">
            <a href = "https://www.facebook.com/upyucatanmx" target = "_blank" rel="noopener noreferrer" 
            class = "btn btn-outline-dark color_btn_redes w-100 d-flex align-items-center justify-content-center gap-2">
            <img class="btn_redes" src="/img/Logos/FACEBOOK_LOGO.svg" alt="Facebook">
            <span>Facebook</span>
        </a>
        </div>

        <!-- Instagram -->
        <div class="col-12 col-sm-6 col-md-4 col-lg-2">
            <button
                class="btn btn-outline-dark color_btn_redes w-100 d-flex align-items-center justify-content-center gap-2">
                <img class="btn_redes" src="/img/Logos/INSTAGRAM_LOGO.svg" alt="Instagram">
                <span>Instagram</span>
            </button>
        </div>

        <!-- Twitter -->
        <div class="col-12 col-sm-6 col-md-4 col-lg-2">
            <button
                class="btn btn-outline-dark color_btn_redes w-100 d-flex align-items-center justify-content-center gap-2">
                <img class="btn_redes" src="/img/Logos/TWITTER_LOGO.svg" alt="Twitter">
                <span>Twitter</span>
            </button>
        </div>
    </div>
</template>
