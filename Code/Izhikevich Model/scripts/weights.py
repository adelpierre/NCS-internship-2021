def create_weights(
    weight_fovea,
    weight_to_LLBN = 1,
    weight_LLBN_input = 1,
    weight_LLBN_recurrent = 1,
    weight_to_EBN = 1,
    weight_LLBN_EBN = 1,
    weight_EBN_IFN = 1,
    weight_IFN_LLBN = 1,
    weight_EBN_TN = 1,
    weight_TN_input = 1,
    weight_TN_recurrent = 1,
    weight_TN_MN = 1
):
    weight_matrix = [weight_fovea, weight_to_LLBN, weight_LLBN_input, weight_LLBN_recurrent, weight_to_EBN, weight_LLBN_EBN, 
                     weight_EBN_IFN, weight_IFN_LLBN, weight_EBN_TN, weight_TN_input, weight_TN_recurrent, weight_TN_MN]
    return weight_matrix