

<!-- view Q&A for mobile -->

                       <!-- Toggle Button active-toggle-producer-QnA-->
                    <button v-if="showQnA"
                       type="button" 
                       class="active-toggle-producer-QnA tertiary-text pt-2 pb-2 border" 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseQnA" 
                       aria-expanded="false" 
                       aria-controls="collapseQnA" 
                       style="font-weight:bold;"
                       @click="checkToShowQnA()">Q&As for {{ specified_producer["producerName"] }} ↑</button>
                   <button v-else
                       type="button" 
                       class="primary-btn-less-round tertiary-text pt-2 pb-2 border" 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseQnA" 
                       aria-expanded="false" 
                       aria-controls="collapseQnA" 
                       style="font-weight:bold;"
                       @click="checkToShowQnA()">Q&As for {{ specified_producer["producerName"] }} ↓</button>
                  
<!-- show Q&A when button is clicked -->
                   <div class="collapse pe-0 ps-0" id="collapseQnA">
                    ...
                   </div>
<script>
export default {

    data() {
        return {
        // to get producer's answered questions
        showQnA: false,
        };
        },
methods: {
// to check if producer QnA should be shown
            checkToShowQnA() {
                if (this.showQnA == true) {
                    this.showQnA = false;
                } 
                else {
                    this.showQnA = true;
                }
            },
        }
    }
</script>    



                 