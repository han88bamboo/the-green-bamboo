<template>
    <!-- Error message if data fails to load -->
    <div v-if="!dataLoaded" class="loading-spinner">
        <div class="text-danger fst-italic fw-bold fs-3" v-if="loadError"> 
            <span>An error occurred while loading data, please try refreshing the page!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="()=>{this.$router.go(0)}">
                <span class="fs-5 fst-italic"> Refresh Page </span>
            </button>
        </div>
    </div>

    <!-- Proof points dashboard -->
    <div v-else>

        <!-- Add rule button -->
        <div class="d-flex justify-content-end mb-3">
            <button class="btn primary-btn" type="button" data-bs-toggle="modal" data-bs-target="#addRuleModal">Add Rule</button>
        </div>

        <!-- Add new rule modal START -->
        <div class="modal fade" id="addRuleModal" tabindex="-1" aria-labelledby="addRuleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="addRuleModalLabel">Add New Rule</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <div class="mb-3">
                                <label for="ruleName" class="form-label">Rule Name</label>
                                <input type="text" class="form-control" id="ruleName" v-model="newRule.ruleName" required>
                            </div>
                            <div class="mb-3">
                                <label for="ruleDesc" class="form-label">Rule Description</label>
                                <textarea class="form-control" id="ruleDesc" v-model="newRule.ruleDesc" required></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="ruleCategory" class="form-label">Rule Category</label>
                                <input type="text" class="form-control" id="ruleCategory" v-model="newRule.ruleCategory" required>
                            </div>
                            <div class="mb-3">
                                <label for="proofPoints" class="form-label">Proof Points</label>
                                <input type="number" class="form-control" id="proofPoints" v-model.number="newRule.proofPoints" step="1" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-primary" @click="addRule" data-bs-dismiss="modal">Add Rule</button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Add new rule modal END -->
        
        <!-- Proof point table -->
        <table class="table">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Rule Name</th>
                <th scope="col">Rule Description</th>
                <th scope="col">Rule Category</th>
                <th scope="col">Proof Points</th>
                <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody class="table-group-divider">
                <tr v-for="rule in rules" :key="rule.id">
                    <th scope="row">{{ rule.id }}</th>
                    <td>
                        <span v-if="editingRuleId != rule.id">{{ rule.ruleName }}</span>
                        <input 
                            v-else 
                            type="text" 
                            v-model="editingRule.ruleName" 
                            style="width: 350px;" 
                        />
                    </td>
                    <td>
                        <span v-if="editingRuleId != rule.id">{{ rule.ruleDesc }}</span>
                        <textarea 
                            v-else 
                            v-model="editingRule.ruleDesc" 
                            style="width: 600px;" 
                        ></textarea>
                    </td>
                    <td>
                        <span v-if="editingRuleId != rule.id">{{ rule.ruleCategory }}</span>
                        <input 
                            v-else 
                            type="text" 
                            v-model="editingRule.ruleCategory" 
                            style="width: 100px;" 
                        />
                    </td>
                    <td>
                        <span v-if="editingRuleId != rule.id">{{ rule.proofPoints }}</span>
                        <!-- downvote min is null and max is -1 -->
                        <input 
                            v-else 
                            type="number" 
                            v-model.number="editingRule.proofPoints" 
                            :min="rule.id == 9 ? null : 1" 
                            :max="rule.id == 9 ? -1 : null"
                            step="1" 
                            style="width: 80px;" 
                        />
                    </td>
                    <td>
                        <!-- Edit button -->
                        <button 
                            v-if ="editingRuleId != rule.id"
                            class="btn btn-primary" 
                            @click="toggleEdit(rule.id)"
                            style="width: 80px;"
                        >
                            Edit
                        </button>

                        <!-- Save and Cancel buttons appear when editing -->
                        <button 
                            v-if="editingRuleId == rule.id" 
                            class="btn btn-success" 
                            @click="saveProofPoints(rule.id)"
                            style="width: 80px;"
                        >
                            Save
                        </button>
                        
                        <button 
                            v-if="editingRuleId == rule.id" 
                            class="btn btn-secondary" 
                            @click="editingRuleId = null"
                            style="width: 80px;"
                        >   
                            Cancel
                        </button>

                        <!-- Delete button appears for rules with id > 15 -->
                        <button 
                            v-if="rule.id > 15" 
                            class="btn btn-danger" 
                            @click="deleteRule(rule.id)"
                            style="width: 80px;"
                        >
                            Delete
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        
    </div>
    

    

</template>

<script>
import { useToast } from 'vue-toastification';


export default {
    name: 'ProofPointsDashboard',
    props: {
        userType: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            dataLoaded: null, // Flag to check if data is loaded

            rules: [], // List to hold the rules data
            editingRuleId: null, // Track the rule being edited
            editingRule: {
                ruleName: '',
                ruleDesc: '',
                ruleCategory: '',
                proofPoints: 0,
            },            
            // New rule data for adding a new rule
            newRule: {
                ruleName: '',
                ruleDesc: '',
                ruleCategory: '',
                proofPoints: 0
            },
        };
    },
    methods: {
        // Retrieve rules data from the API
        async fetchRules() {
        try {
            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/proofPoints/getPointSystemRules`);
            this.rules = response.data; // Store the rules data in the component's state
            this.dataLoaded = true; // Set dataLoaded to true after fetching data
        } catch (error) {
            console.error('Error fetching rules:', error);
            this.dataLoaded = false; // Set dataLoaded to false on error
            
        }
        },

        // Toggle edit mode for a rule
        toggleEdit(ruleId) {
            this.editingRuleId = ruleId; // Set the rule ID to be edited
            const rule = this.rules.find(r => r.id === ruleId); // Find the rule being edited
            if (rule) {
                this.editingRule.ruleName = rule.ruleName; // Set the rule name for editing
                this.editingRule.ruleDesc = rule.ruleDesc; // Set the rule description for editing
                this.editingRule.ruleCategory = rule.ruleCategory; // Set the rule category for editing
                this.editingRule.proofPoints = rule.proofPoints; // Set the proof points for editing
            }
        },

        // Save edited proof points to the API
        async saveProofPoints(ruleId) {
            try {
                const response = await this.$axios.put(`${process.env.VUE_APP_API_URL}/proofPoints/updatePointSystemRule`, {
                    'userType' : this.userType,
                    'ruleId' : ruleId,
                    'rule_name' : this.editingRule.ruleName,
                    'rule_desc' : this.editingRule.ruleDesc,
                    'rule_category' : this.editingRule.ruleCategory,
                    'proof_points' : this.editingRule.proofPoints
                });

                if (response.status == 201) {
                    this.fetchRules(); // Refresh the rules after saving
                    this.editingRuleId = null; // Reset editing state after saving
                    const toast = useToast();
                    toast.success(
                        "Proof Points Updated Successfully",
                    );
                }
                
            } catch (error) {
                console.error('Error saving proof points:', error);
                const toast = useToast();

                if (error.response && error.response.status != 500) {
                    toast.error(
                        error.response.data.message
                    );
                } else {
                    toast.error(
                        "Error updating proof points, please try again later.",
                    );
                } 
            }
        },

        // Delete a rule from the API
        async deleteRule(ruleId) {
            try {
                const response = await this.$axios.delete(`${process.env.VUE_APP_API_URL}/proofPoints/deletePointSystemRule`, {
                    data: {
                        'userType' : this.userType,
                        'ruleId' : ruleId
                    }
                });

                if (response.status == 200) {
                    this.fetchRules(); // Refresh the rules after deletion
                    const toast = useToast();
                    toast.success(
                        "Proof Points Deleted Successfully",
                    );
                }
                
            } catch (error) {
                console.error('Error deleting rule:', error);
                const toast = useToast();
                if (error.response && error.response.status == 400) {
                    toast.error(
                        error.response.data.message
                    );
                } else {
                    toast.error(
                        "Error deleting proof points, please try again later.",
                    );
                }
            }
        },

        // Add new rule to the API
        async addRule() {
            // Check if all fields are filled
            if (this.newRule.ruleName && this.newRule.ruleDesc && this.newRule.ruleCategory && this.newRule.proofPoints) {
                try {
                    const response =await this.$axios.post(`${process.env.VUE_APP_API_URL}/proofPoints/createPointSystemRule`, {
                        'userType' : this.userType,
                        'rule_name' : this.newRule.ruleName,
                        'rule_desc' : this.newRule.ruleDesc,
                        'rule_category' : this.newRule.ruleCategory,
                        'proof_points' : this.newRule.proofPoints
                    });

                    if (response.status == 201) {
                        this.fetchRules(); // Refresh the rules after adding
                        const toast = useToast();
                        toast.success(
                            "New rule added successfully",
                        );
                    }
                    
                } catch (error) {
                    console.error('Error adding rule:', error);
                    const toast = useToast();
                    if (error.response && error.response.status != 500) {
                        toast.error(
                            error.response.data.message
                        );
                    } else {
                        toast.error(
                            "Error adding proof points, please try again later.",
                        );
                    }
                }
            } else {
                const toast = useToast();
                toast.error(
                    "Please fill all fields before adding a new rule.",
                );
            }
        }
    },
    mounted() {
        // Code to run when the component is mounted
        this.fetchRules(); // Fetch rules data when the component is mounted
    }
};
</script>