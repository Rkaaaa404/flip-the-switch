Ecological Informatics 95 (2026) 103711 



Contents lists available at ScienceDirect 

# Ecological Informatics 

journal homepage: www.elsevier.com/locate/ecolinf 



## Deep feature optimization for enhanced fish freshness assessment 



Phi-Hung Hoang, Nam-Thuan Trinh, Van-Manh Tran, Thi-Thu-Hong Phan ∗ 

_AIT laboratory, Faculty of Artificial Intelligence, FPT University, Da Nang, 550000, Viet Nam_ 

|A R T I C L E I N F O|A B S T R A C T|
|---|---|
|Code availability:GitHub Repository<br>_Keywords:_<br>Automated classification<br>Deep visual features<br>Ensemble-based feature selection<br>Feature optimization<br>Fish eye freshness|Assessing fish eye freshness is vital for ensuring food safety and minimizing economic losses in the seafood in-<br>dustry. However, traditional sensory evaluation methods remain subjective, time-consuming, and inconsistent.<br>Despite recent advancements in deep learning for automating visual freshness prediction, challenges related to<br>accuracy and feature transparency persist. This study introduces a unified three-stage framework that refines<br>and leverages deep visual representations for reliable fish eye freshness assessment. First, five state-of-the-art<br>vision architectures – ResNet-50, DenseNet121, EfficientNet-B0, ConvNeXt-Base, and Swin-Tiny – are fine-tuned<br>to establish a strong baseline. Next, multi-level deep features extracted from these backbones are used to train<br>seven classical machine learning classifiers, integrating deep and traditional decision mechanisms. Finally,<br>feature selection methods based on Light Gradient Boosting Machine (LGBM), Random Forest, and Lasso are<br>utilized to identify a compact and informative subset of features. Experiments conducted on the Freshness of<br>the Fish Eyes (FFE) dataset demonstrate that the best configuration – combining Swin-Tiny features, a Random<br>Forest classifier, and LGBM-based feature selection – achieves an accuracy of 85.99%, outperforming recent<br>studies on the same dataset by 8.69–22.78%. These findings confirm the effectiveness and generalizability of<br>the proposed framework for visual quality evaluation tasks.|



### **1. Introduction** 

Fish is an essential component of the global diet, providing highquality protein and vital nutrients that contribute significantly to human health (Tidwell and Allan, 2001; Chen et al., 2022). Beyond its nutritional value, the fisheries sector also plays a crucial economic role in global food security and trade. However, fish is an inherently perishable commodity, and improper handling or storage can rapidly deteriorate its freshness, leading to both economic losses and potential health risks. Traditionally, freshness evaluation has relied on sensory inspection by trained experts, who assess the eyes, gills, skin, and odor. Although practical, these subjective methods are time-consuming, inconsistent, and difficult to scale for large quantities of fish, particularly under industrial conditions (Hassoun and Karoui, 2017; Prabhakar et al., 2020). Therefore, developing rapid, accurate, and automated techniques for assessing fish eye freshness has become essential to ensure food safety and improve management efficiency in the seafood industry. 

To address these challenges, researchers have explored a wide range of image-based approaches for objective and automated evaluation. Early studies primarily employed handcrafted visual descriptors – such as color features, local binary patterns (LBP), and gray-level co-occurrence matrices (GLCM) – combined with machine learning 

classifiers to infer freshness levels (Medeiros et al., 2021; Syarwani et al., 2022; Arora et al., 2022; Hoang et al., 2026). While these methods achieved promising results, their performance heavily depended on manual feature design and often lacked robustness across diverse imaging conditions. This limitation has motivated the adoption of deep learning approaches that can automatically learn hierarchical and discriminative representations directly from raw images. 

The advent of deep learning has revolutionized visual analysis by enabling automatic feature learning directly from raw images. Several convolutional neural network (CNN)-based architectures and lightweight variants have been applied to fish eye freshness prediction (Prasetyo et al., 2022b; Jayasundara et al., 2023; Cahyo and Al-Ghiffary, 2024; Khaleel et al., 2024; Sanga et al., 2024). However, despite clear progress, the Freshness of the Fish Eyes (FFE) dataset remains particularly challenging due to its high variability involving eight fish species across three freshness levels. Furthermore, the images were captured using mobile phones under uncontrolled lighting and background conditions, which explains why existing deep models have achieved only moderate accuracies of 63% and 77% in the studies of Prasetyo et al. (2022b), Yildiz et al. (2024). This suggests that distinguishing subtle inter-class differences in eye appearance still demands more discriminative and interpretable representations. 

> ∗ Corresponding author. 

_E-mail addresses:_ hunghpde180523@fpt.edu.vn (P.-H. Hoang), thuantnde180305@fpt.edu.vn (N.-T. Trinh), manhtvde180090@fpt.edu.vn (V.-M. Tran), hongptt11@fe.edu.vn (T.-T.-H. Phan). 

https://doi.org/10.1016/j.ecoinf.2026.103711 Received 5 November 2025; Received in revised form 8 February 2026; Accepted 13 March 2026 Available online 14 March 2026 

1574-9541/© 2026 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/). 

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 

Moreover, existing studies often evaluate deep networks in an endto-end manner, without explicitly analyzing how feature abstraction levels or feature selection mechanisms affect performance. For instance, Prasetyo et al. (2022b) directly used CNN or pre-trained models for classification without optimizing or interpreting the extracted embeddings, while Yildiz et al. (2024) focused solely on feature extraction from CNNs without systematic dimensionality refinement. 

In this context, this study introduces a comprehensive deep feature optimization framework that systematically evaluates and refines learned representations for fish eye freshness assessment. Specifically, we: 

- Evaluate several state-of-the-art vision backbones – including ResNet-50, DenseNet-121, EfficientNet-B0, Swin-Tiny, and ConvNeXt-Base – to establish a robust baseline for image-based freshness classification. 

- Apply Grad-CAM visualization to interpret and compare model behavior across architectures, without guiding the framework design. 

- Extract deep embeddings from different abstraction levels of each backbone and evaluate their discriminative power using classical machine learning classifiers. 

- Investigate embedded feature selection methods – LGBM (boosting), Random Forest (bagging), and Lasso (L1 regularization) – to identify compact and discriminative subsets of features. 

To the best of our knowledge, this is the first study to systematically analyze how deep feature abstraction and embedded feature optimization jointly affect fish eye freshness classification performance on the public FFE dataset. The proposed framework demonstrates improved accuracy and enhanced interpretability, while maintaining computational efficiency suitable for practical applications. 

The rest of the paper is organized as follows. Section 2 reviews related literature. Section 3 presents the proposed methodology, covering the main approaches and techniques used. Section 4 describes the experimental setup. Section 5 presents the results and offers a comprehensive discussion of the findings. Finally, Section 6 concludes the study and suggests directions for future research. 

### **2. Related works** 

Early computer vision approaches for fish eye freshness assessment primarily relied on manually engineered features extracted from digital images to capture visual degradation in the eyes, gills, and skin. Color-based descriptors were dominant, often computed as statistical measures or histograms in RGB, HSV, HSI, and CIELAB spaces to quantify discoloration. For instance, Medeiros et al. (2021) extracted a comprehensive set of colorimetric parameters from multiple color spaces and achieved 100% accuracy in classifying tuna and salmon freshness using an AutoML framework. Texture features like the GLCM and LBP were also used to represent surface variations such as eye cloudiness. Syarwani et al. (2022) combined HSV color features with GLCM descriptors, attaining 94.28% accuracy for Nile Tilapia freshness using a SVM. Arora et al. (2022) further advanced feature fusion by computing a unified ‘‘Q-score’’ from weighted visual features of the gills, eyes, and skin, achieving 98.07% accuracy. More recently, Hoang et al. (2026) demonstrated that a systematic fusion of handcrafted color and texture features could achieve 77.56% accuracy on the FFE dataset, highlighting the potential of optimized feature integration for improving machine learning-based fish eye freshness classification. 

Building on these foundations, deep learning approaches were developed to extract discriminative features automatically. Lightweight architectures such as MobileNetV1 bottleneck with Expansion (MB-BE) achieved 63.21% accuracy on the FFE dataset, illustrating the trade-off 

between efficiency and performance (Prasetyo et al., 2022b). Jayasundara et al. (2023) developed FishNET-S for Indian Sardinella focusing on fish eyes and FishNET-T for Yellowfin Tuna focusing on fish meat, achieving 84.1% and 68.3% accuracy, respectively. Concurrently, many studies focused on well-established CNN architectures such as ResNet and DenseNet. By leveraging pre-trained models and data fusion techniques, these approaches reported exceptional classification accuracies ranging from approximately 93% to 100% (Cahyo and Al-Ghiffary, 2024; Khaleel et al., 2024; Sanga et al., 2024). 

Recent research has explored advanced hybrid models that combine multiple neural network architectures to improve fish eye freshness assessment. Rodrigues et al. (2024) were the first to apply Vision transformers (ViT) in this context. Their two-stage system first segmented the fish eye region with high performance, achieving a 98.77% detection rate and 85.7% IoU using a Segformer, before classification with a ViT resulted in 80.8% accuracy. Hybrid architectures have also been explored, with Biswas et al. (2025) proposing a CNN–LSTM model that integrates spatial and sequential information and uses LIME for interpretability, achieving 86% accuracy. Peries et al. (2025) conducted a systematic comparison of multiple pre-trained architectures across whole fish, fish eyes, and fish gills, with the highest accuracy of 99.13% achieved on gills using DenseNet121. 

Hybrid frameworks have become an important direction in automated fish eye freshness assessment, employing deep learning to generate rich feature representations and traditional machine learning to perform classification. This combination leverages the strengths of both approaches, balancing accuracy with efficiency and interpretability. For example, Kılıçarslan et al. (2024) extracted features from pre-trained models and classified them with traditional algorithms, achieving a 100% success rate. Similarly, Yildiz et al. (2024) applied pre-trained CNNs to the FFE dataset and found that combining VGG19 features with an ANN yielded the highest accuracy of 77.3%. Extending this concept, Lanjewar and Panchbhai (2024) employed a NasNet–LSTM architecture for feature extraction along with data balancing and feature selection techniques, achieving Matthew’s correlation coefficient (MCC) and Cohen’s kappa coefficient (KC) scores of 99.1%. 

Another advanced strategy is multimodal data fusion, which integrates information from different sensors to provide a more comprehensive representation of freshness. Hardy et al. (2024) fused fluorescence, visible, and near-infrared spectroscopy data, reporting nearly perfect accuracies of 99.5% compared to single-mode analyses of 77.1%. Similarly, Balım et al. (2025) combined RGB images with laser reflectance data, achieving 88.44% accuracy. 

A review of the literature also highlights several common limitations, as summarized in Table 1. Many studies rely on small or private datasets collected under ideal laboratory conditions, such as controlled lighting and background, which hinders fair comparison and raises concerns about generalizability. Methodologically, much of the research focuses on a single anatomical region such as the eye or relies exclusively on either handcrafted features or deep learning, rarely exploring a systematic combination of both. Furthermore, some hybrid frameworks use conventional CNN architectures that may not fully capture complex visual cues. 

These limitations highlight the need for a systematic framework that not only evaluates deep feature representations across different abstraction levels but also incorporates feature optimization techniques to achieve compact, interpretable, and generalizable freshness classification. 

### **3. Methodology** 

### _3.1. Overview of the proposed approach_ 

To systematically evaluate and overcome the inherent difficulty of accurately classifying fish eye freshness from imaging data, this 

2 

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 

**Table 1** 

Summary of recent studies on fish eye freshness assessment. 

|Studies|Methodology|Accuracy|Limitations|
|---|---|---|---|
|Medeiros<br>et al. (2021)|Colorimetric features from<br>multiple spaces classified with<br>AutoML|100%|Limited number of tuna and<br>salmon samples. Freshness was<br>assessed only using color features,<br>which may overlook other<br>important indicators|
|Syarwani<br>et al. (2022)|HSV + GLCM features with SVM<br>classifier|94.28%|Small sample of Nile Tilapia eyes<br>and gills in lab conditions|
|Arora et al.<br>(2022)|Fused gill, eye, and skin features<br>into a single Q-score|98.07%|Limited Rohu data reduces<br>generalizability across species and<br>environments. Segmentation<br>employed simple traditional<br>image processing|
|Prasetyo<br>et al. (2022b)|Proposed a lightweight CNN<br>(MB-BE)|63.21%|Low overall accuracy due to<br>lightweight design and limited<br>feature representation and limited<br>generalization|
|Jayasundara<br>et al. (2023)|Proposed two specialized CNNs:<br>FishNET-S (for small fish eyes)<br>and FishNET-T (for large fish<br>meat)|90% (FishNET-S), 100%<br>(FishNET-T)|Two separate models for different<br>fish species limit generalization<br>and controlled data reduce<br>robustness in real-world settings|
|Cahyo and<br>Al-Ghiffary<br>(2024)|ResNet101 + GLCM features|100%|The research focused on a single<br>species with limited data,<br>employing conventional image<br>processing for segmentation in<br>controlled lab lighting|
|Khaleel et al.<br>(2024),<br>Sanga et al.<br>(2024)|ResNet18 + image fusion;<br>Compared VGG19, MobileNetV2,<br>DenseNet201, ResNet50|93%, 100%|Considering only two freshness<br>classes, the deep learning model’s<br>interpretability remains limited|
|Rodrigues<br>et al. (2024)|Segformer for segmentation + ViT<br>for classification|98.77% detection, 85.7%<br>IoU, 80.8% accuracy|Using transformers for<br>segmentation and classification<br>requires high computational<br>resources|
|Biswas et al.<br>(2025)|CNN–LSTM integrating<br>spatial–sequential features with<br>LIME interpretability|86%|The integration of CNN and LSTM<br>on a single-species dataset with<br>binary classification increases<br>model complexity|
|Peries et al.<br>(2025)|Evaluated CNNs and pre-trained<br>models on fish eyes, gills, and<br>whole fish|99.13% (DenseNet121, gill)|Low image resolution, binary<br>classification, single-region data,<br>and limited explainability reduce<br>generalization|
|Kılıçarslan<br>et al. (2024)|Features from MobileNetV2,<br>Xception, VGG16 + ML classifiers<br>(SVM, LR, ANN, RF)|100%|Single-species dataset under<br>controlled conditions, binary<br>classification, and limited<br>explainability|
|Yildiz et al.<br>(2024)|VGG19 & SqueezeNet features +<br>ML classifiers (KNN, RF, SVM,<br>LR, ANN)|77.3%|Extracted features are insufficient<br>to capture complex, long-range<br>dependencies in the data|
|Lanjewar and<br>Panchbhai<br>(2024)|NasNet–LSTM hybrid with<br>SMOTEENN balancing and feature<br>selection|99.1% (MCC & KC scores)|Focusing only on the eye region<br>and using a CNN–LSTM hybrid,<br>the model becomes more complex<br>and harder to interpret|
|Hardy et al.<br>(2024)|Fused fluorescence + VIS–NIR<br>data via LDA, KNN, and ensemble<br>bagged trees|99.5%|Limited fish samples, generous<br>classification metric, controlled<br>lab environment, and<br>single-species focus|
|Balım et al.<br>(2025)|Laser + CNN feature fusion with<br>SVM, MLP, RF classifiers|88.44%|The evaluation used only<br>mackerel and a 940 nm laser<br>wavelength, making<br>generalization to other species<br>and conditions difficult|



study proposes a novel and progressive framework that integrates modern deep learning and machine learning techniques within a unified training–evaluation pipeline (Fig. 1). The framework is designed not merely as a comparative setup but as a structured exploration of how recent advances in vision architectures and hybrid learning strategies can be effectively exploited for fine-grained classification tasks. 

In the first stage, a series of representative deep learning models – ResNet-50, DenseNet-121, EfficientNet-B0, Swin-Tiny, and ConvNeXtBase – were fine-tuned using Random search for hyperparameter optimization. These architectures were deliberately chosen to capture diverse design philosophies, ranging from conventional convolutional networks to transformer-based and convolution–transformer hybrid 

3 



<!-- Start of picture text -->
ConvNext-Base Embedded ConvNeXt-Base<br>ror<br>ResNet-50 Random Forest (RF)<br>DenseNet-121 LightGBM (LGBM)<br>a<br>T<br>== Fish Eyes<br>Trained Deep<br>Feature Importance-Baseda Deep Features a<br>(Embedded) Extraction Test Set<br><!-- End of picture text -->

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 

ResNet-50 architecture consists of 50 layers arranged in four residual stages with downsampling at the start of stages 2, 3, and 4. Each bottleneck block includes 1 × 1, 3 × 3, and 1 × 1 convolutions, while the network begins with a 7 × 7 convolution and max pooling, and concludes with global average pooling and a fully connected classification layer. 

### _3.2.2. DenseNet-121_ 

Dense Convolutional Networks (DenseNets) (Huang et al., 2017) introduce dense connectivity to enhance feature reuse and parameter efficiency. Instead of summing residuals as in ResNet, each layer in a DenseNet concatenates its output with all preceding feature maps within the same block. DenseNet-121 applies this principle across multiple dense blocks separated by transition layers that downsample and reduce channels using 1 × 1 convolutions and average pooling. Each dense layer consists of batch normalization, ReLU activation, and convolution, followed by global average pooling and a fully connected classification layer. 

### _3.2.3. EfficientNet-B0_ 

EfficientNet (Tan and Le, 2020) introduces a compound scaling method that uniformly balances network depth, width, and input resolution using learned coefficients, addressing the inefficiency of scaling a single dimension. EfficientNet-B0 serves as the baseline architecture discovered through neural architecture search, optimized for both accuracy and computational cost. Its primary building block, the MBConv, employs an inverted bottleneck with channel expansion, depthwise separable convolution, and Squeeze-and-Excitation attention. The model follows a standard multi-stage ConvNet structure, concluding with global average pooling and a fully connected classification layer. 

### _3.2.4. Swin Transformer-Tiny (Swin-Tiny)_ 

The Swin Transformer (Liu et al., 2021) introduces a hierarchical Vision Transformer that improves efficiency for high-resolution and dense prediction tasks. It builds hierarchical feature maps through patch merging and applies window-based self-attention within local regions for linear computational complexity. The Swin TransformerTiny (Swin-T) variant uses shifted windows to capture cross-window dependencies, with patch merging between stages to reduce tokens and expand feature dimensions before global pooling and classification. 

### _3.2.5. ConvNeXt-Base_ 

ConvNeXt (Liu et al., 2022) revisits conventional ConvNet architectures by incorporating design principles from Vision Transformers to achieve comparable performance while maintaining convolutional efficiency and inductive biases. ConvNeXt-Base follows a ResNet-like stage structure with key modifications, including a larger-stride stem, non-overlapping patch-like convolutions, large-kernel depthwise layers, and inverted bottlenecks inspired by Transformer MLPs. It replaces batch normalization with layer normalization and applies downsampling between stages, forming a hierarchical yet purely convolutional architecture. 

### _3.3. Deep feature extraction strategy_ 

The effectiveness of deep features hinges on a crucial trade-off: mid-level layers retain local, fine-grained spatial details necessary for subtle cues, such as texture and glossiness, while high-level layers capture richer, more abstract semantic patterns. To systematically identify the most informative representations for assessing fish eye freshness, features from both mid-level and high-level stages of each fine-tuned model were independently extracted. These representations were subsequently condensed using GAP, a standard technique that creates compact, fixed-length vectors from feature maps. This approach preserves essential global information while significantly reducing feature dimensionality and computational complexity for the downstream traditional machine learning models. The specific candidate extraction points for each model, along with their detailed rationale, are summarized in Table 2. 

### _3.4. Explainability with grad-CAM_ 

Grad-CAM (Gradient-weighted Class Activation Mapping) is a visualization technique used to interpret the decision-making process of deep learning models by highlighting the important regions in the input image that contribute most to the model’s prediction (Selvaraju et al., 2017). Grad-CAM computes the gradients of the target class score with respect to the feature maps of the last convolutional layer (in CNNs) or the corresponding representation layer (in Transformers) to generate a heatmap indicating the areas of focus. 

In this study, Grad-CAM is applied to both CNN- and Transformerbased models to analyze the visual regions influencing their classification decisions. For CNN architectures (ResNet-50, DenseNet-121, EfficientNet-B0, and ConvNeXt-Base), Grad-CAM is computed using the feature maps from the final convolutional layer, which preserves high-level semantic information while retaining spatial structure. 

For the Transformer-based model (Swin-Tiny), Grad-CAM requires a specific adaptation due to its hierarchical and non-convolutional design. In this case, we use the output of the final Swin Transformer block in the last stage (Stage 4), where discriminative semantic representations are formed prior to classification. Gradients of the target class score are backpropagated with respect to the patch-level feature representations at this stage. 

As the Swin Transformer produces feature maps in a channel-last format ( _, , , _ ), where __ , __ , __ , and __ denote the batch size, feature map height, feature map width, and number of channels, respectively, a dimension permutation is applied to convert them into the standard channel-first format ( _, , , _ ) before computing the class activation maps, ensuring a consistent Grad-CAM formulation across CNN and Transformer architectures. 

### _3.5. Embedded feature selection strategy_ 

In this study, we adopt embedded feature selection as our primary approach. Embedded methods integrate the assessment of feature relevance directly into the model training process, unlike filter and wrapper techniques, which treat feature selection as a separate preprocessing step. By evaluating predictive value during model construction (Fig. 2), embedded methods produce a compact, model-specific subset of features that enhances both robustness and generalization. Our choice of embedded feature selection is motivated by prior evidence demonstrating its effectiveness across diverse domains. For example, in water quality index (WQI) prediction (Lap et al., 2023) and rice seed purity classification (Phan and Nguyen, 2025), embedded techniques consistently outperformed filter and wrapper approaches in terms of predictive performance and feature selection capability. Considering the high dimensionality and complexity of deep features extracted for fish eye freshness assessment, embedded methods are expected to provide a reliable and efficient strategy for selecting the most informative features. 

To perform comprehensive feature optimization, we employ three complementary embedded methods: Lasso regression (L1) - Regularization), RF, and LGBM. These techniques cover the major mechanisms of embedded feature selection: 

### **_1. Tree-based ensemble selection (Bagging & Boosting)_** 

- **Random forest (Bagging):** RF averages importance across many independent decision trees. Features are ranked based on their ability to improve node purity (e.g., Gini impurity), providing a stable and generalized measure of relevance. 

- **LightGBM (Boosting):** LGBM sequentially builds trees, focusing on features that provide the greatest Gain (reduction in loss) at each split. This effectively captures complex non-linear relationships and the predictive power of features. 

5 



<!-- Start of picture text -->
Selection of Learning Algorithm<br>Subset and Performance<br><!-- End of picture text -->



<!-- Start of picture text -->
Eleutheronema _ Rastrelliger Upeneus Oreochromis — Oreochromis Johnius Nibea<br>Tetradactylum Faughni Moluccensis = Mossambicus Niloticus Trachycephalus —_—Allbiflora Chanos Chanos<br>= . peta - a) 7 ’ ]<br>= 5 4‘ %‘ot co. ‘i ©<br>=7 on ee ae :<br>3S e ‘ ie i 4 f _= ¥ w<br>aiA >» ay<br>S * 7" SD Be y ait<br>o fe } \ uO) K q<br><!-- End of picture text -->

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 

**Table 5** 

|Hyperparameter search space for cla|ssical machine learning mode|ls used in the experiments.|
|---|---|---|
|Model|Hyperparameter|Search Space/Values|
|Logistic Regression (LR)|penalty<br>C<br>solver<br>max_iter|l1, l2<br>0.01, 0.1, 1.0, 10, 100<br>liblinear, saga<br>Integer range [300, 799]|
|K-Nearest Neighbors (KNN)|n_neighbors<br>weights<br>metric<br>algorithm|3, 5, 7, 9, 11, 15, 17, 19, 21, 23<br>uniform, distance<br>euclidean, manhattan, chebyshev, minkowski<br>auto, ball_tree, kd_tree, brute|
||kernel<br>|linear, poly, rbf<br>|
|SuortVectorMachine(SVM)|C|0.01, 0.1, 1, 10, 100|
|pp|gamma<br>coef0|scale, auto<br>0.0, 0.01, 0.1 (poly kernel only)|
||n_estimators|Integer range [10, 500]|
|Random Forest (RF)|max_depth|Integer range [2, 49]|
||criterion|gini, entropy|
||n_estimators<br>criterion<br>|Integer range [10, 500]<br>gini, entropy<br>|
||max_depth|None, 10, 15, 20, 25, 30, 35, 40, 50|
|Extra Trees (ET)|min_samples_split|2, 3, 5, 7, 9, 11|
||min_samples_leaf|1, 3, 5, 8, 9, 11|
||bootstrap<br>|True, False<br>|
||max_leaf_nodes|None, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13|
||boosting_type|gbdt, dart|
||n_estimators|Integer range [10, 500]|
|LightGBM (LGBM)|learning_rate<br>num_leaves<br>|0.001, 0.01, 0.1, 1, 10<br>Integer range [15, 49]<br>|
||max_depth|Integer range [2, 49]|
||class_weight|balanced, None|
||iterations|Integer range [300, 999]|
|CatBoost (CB)|learning_rate<br>l2_leaf_reg<br>grow_policy|0.03, 0.04, 0.05, 0.1, 0.2, 0.3<br>1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21<br>SymmetricTree, Depthwise|
||hidden_layer_sizes<br>activation|Integer range [64, 256] (single hidden layer)<br>logistic, tanh, relu|
||solver|adam, sgd, lbfgs|
|Neural Network (ANN)|alpha|0.0001, 0.001, 0.01, 0.1<br>|
||max_iter|Integer range [800, 1700]|
||learning_rate|constant, adaptive, invscaling|
||early_stopping|True|



Among all evaluated models, the Swin Transformer-Tiny (SwinTiny) achieved the highest accuracy of 84.85%, outperforming the other architectures. This superior performance can be attributed to its hierarchical transformer design with window-based self-attention, which effectively captures both fine-grained local textures (e.g., lens cloudiness and surface opacity) and broader contextual cues (e.g., gradual color transitions and spatial consistency) relevant to fish-eye freshness. Unlike conventional convolutional models with fixed receptive fields, Swin-Tiny enables more effective modeling of these discriminative visual characteristics through localized self-attention and shifted windows, thereby contributing to its improved classification performance. 

The ConvNeXt-Base model reached a closely similar accuracy of 84.51%. This strong performance can be attributed to its modernized convolutional design, which incorporates principles inspired by vision transformers. Features such as larger kernel sizes, updated block structures, and enhanced normalization strategies allow ConvNeXt to capture both fine-grained textures and larger spatial patterns effectively, resulting in performance comparable to transformer-based models. 

EfficientNet-B0, DenseNet-121, and ResNet-50 are considered midlevel models, achieving accuracies of 81.32%, 80.75%, and 80.07%, respectively. EfficientNet-B0 leverages compound scaling to uniformly adjust depth, width, and resolution, capturing rich visual features efficiently. Its MBConv blocks with squeeze-and-excitation further enhance feature representation by emphasizing informative channels. DenseNet121 and ResNet-50 rely on conventional architectures that effectively extract general features but may be limited in modeling complex spatial 

#### **Table 6** 

Performance of different DL models for fish eye freshness assessment (%). 

|Model|Accuracy|Precision|Recall|F1-score|
|---|---|---|---|---|
|ConvNeXt-Base|**84.51**|83.73|83.60|83.62|
|Swin-Tiny|**84.85**|**84.08**|**84.08**|**83.93**|
|EfficientNet-B0|81.32|80.55|80.04|80.19|
|DenseNet-121|80.75|79.91|80.04|79.97|
|ResNet-50|80.07|79.21|79.59|79.33|



relationships and subtle textures, which are important for fine-grained freshness assessment. 

### _5.1.1. Confusion matrix analysis_ 

To gain a clearer understanding of the specific inter-class misclassifications made by the models, we provide a detailed analysis of the Confusion Matrices (CM) for the two best-performing architectures: ConvNeXt-Base and Swin-Tiny, as shown in Fig. 4. 

The analysis revealed that both models were highly effective at identifying the extreme classes. Swin-Tiny accurately classified 338 ‘‘ _Highly fresh_ ’’ samples, while ConvNeXt-Base performed comparably well by correctly identifying 336 samples. However, the models diverged in handling the critical boundary zones. ConvNeXt-Base was marginally better at identifying the difficult middle class, correctly classifying 206 ‘‘ _Fresh_ ’’ samples compared to Swin-Tiny’s 196. At the same time, it demonstrated a weakness in risk assessment, as it misclassified 13 truly ‘‘ _Not fresh_ ’’ samples as ‘‘ _Highly fresh_ ’’. In contrast, Swin-Tiny was more 

8 



<!-- Start of picture text -->
g 300<br>4 19 1<br>z20<br>i 200<br>FS52cFy& 28 37 180<br>~ 100<br>E13 28 200<br>z -50<br>Highly Fresh PredictedFreshLabels Not Fresh<br><!-- End of picture text -->



<!-- Start of picture text -->
4% 300<br>re 338 20 8<br>- 260<br>F 200<br>3&jotFf© 34 196 41 180<br>toc<br>é 6 24 211<br>3 - 50<br>Highly Fresh PredictedFreshLabels Not Fresh<br><!-- End of picture text -->

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 



**Fig. 5.** Grad-CAM visualizations highlighting the image regions attended to by different deep learning models during fish eye freshness classification. 

**Table 7** 

Performance of ML classifiers on deep features extracted from Swin-Tiny (Stage 3 vs. Stage 4) (%). 

|Model|Stage 3|(middle-lev|el features)||Stage 4|(high-level|features)||
|---|---|---|---|---|---|---|---|---|
||ACC|Recall|Precision|F1|ACC|Recall|Precision|F1|
|LR|81.89|81.89|81.87|81.82|85.19|85.19|85.34|85.24|
|KNN|83.03|81.03|83.12|83.10|85.65|85.65|85.67|85.64|
|SVM|**84.97**|84.97|84.99|**84.98**|85.65|85.65|85.58|85.59|
|ANN|82.23|82.23|82.36|82.26|85.54|85.54|85.67|85.57|
|RF|79.95|79.95|79.75|79.69|85.31|85.31|85.48|85.38|
|ET|80.75|80.75|80.52|80.43|**85.88**|**85.88**|**85.91**|**85.89**|
|LGBM|81.66|81.66|81.55|81.59|85.08|85.08|85.15|85.10|
|CB|80.64|80.64|80.50|80.54|84.28|84.28|84.35|84.30|



resulting in an overall accuracy of 85.88%. Compared to the SwinTiny model, this approach improved the classification of the Fresh class by approximately 6.6%, indicating that the tree-based classifier can better handle subtle variations between adjacent categories. Although a slight decrease was observed for the Not Fresh class, the results remain competitive and more evenly distributed. These findings suggest that the Stage 4 embeddings of Swin-Tiny provide sufficiently discriminative representations, and when combined with ET, they enhance generalization performance. 

Following the selection of the best-performing backbone, we also conducted experiments using feature embeddings extracted from all other deep architectures to verify the generality of this hybrid approach. The same feature-extraction and training protocol was consistently applied across ConvNeXt, EfficientNet, ResNet-50, and DenseNet to ensure comparability. Importantly, the improvement observed with Swin-Tiny was not an isolated case. As shown in Table 8, the hybrid deep feature-based learning strategy consistently enhanced performance across all evaluated architectures. For instance, ConvNeXtBase improved from 84.51% to 85.19%, while more traditional CNNs showed even greater gains—ResNet-50 increased from 80.07% to 83.14%, and DenseNet-121 from 80.75% to 83.49%. These results confirm that the fully connected layers in DL models may not always provide the most effective decision boundaries, and that classical machine 

learning classifiers can more efficiently exploit the rich representations generated by deep backbones. 

A crucial observation from Table 8 is that, across all evaluated architectures, the most effective features were consistently extracted from the higher-level representation layers. This pattern reinforces the earlier finding from Swin-Tiny that deeper embeddings provide superior discriminative power compared to those from intermediate levels. ET achieved the best results with transformer-derived representations extracted from Swin-Tiny (768 features) and ConvNeXt-Base (1024 features), highlighting its capacity to model complex, high-level dependencies. KNN performed effectively with DenseNet-121 features (1024 features), consistent with DenseNet’s feature-reuse mechanism that forms compact and locally coherent clusters in the embedding space. LGBM showed strong performance with ResNet-50 features (2048 features), demonstrating its robustness in capturing non-linear relationships within high-dimensional data. Finally, SVM achieved the best results with EfficientNet-B0 features (320 features), as its compound scaling and MBConv design produce compact and regularized feature spaces that enhance margin-based separation. 

### _5.3. Performance of selected deep features_ 

The analysis in Section 5.2 demonstrated that high-level features extracted from deep architectures, when used with classical machine 

10 



<!-- Start of picture text -->
G2 300 TTT hGssG>s44sh ii<br>le2>= 23 8 To<br>+<br>250<br>a 200<br>3 =<br>13 23 34<br>£g ire ~ 150 —_——_<br>~ 100 ou,<br>$8<br>ire 4 32<br>6 ~ 50<br>Fd<br>Highly Fresh Fresh Not Fresh<br>Predicted Labels<br><!-- End of picture text -->

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 

**Table 12** 

Best-performing feature subsets selected by LGBM (boosting) for each deep learning model (%). 

|Model|Feature subset|Dimension|Best classifier|Accuracy|
|---|---|---|---|---|
|Swin-Tiny|10%|77|RF|**85.99**|
|ConvNeXt-Base|10%|103|SVM|85.31|
|DenseNet-121|10%|103|ET|83.60|
|ResNet-50|10%|205|LGBM|83.49|
|EfficientNet-B0|50%|160|KNN|82.35|



properties. As a gradient boosting-based method, LGBM performs feature selection implicitly through gradient-based optimization, where feature importance is determined by the cumulative contribution of each feature to loss reduction across all boosting iterations rather than by isolated splits. Its histogram-based splitting strategy enables efficient evaluation of candidate thresholds, while the leaf-wise tree growth prioritizes highly discriminative splits, allowing LGBM to capture complex nonlinear relationships and subtle feature interactions that are critical for the target task. In contrast, RF evaluates feature importance mainly based on impurity or variance reduction across independently trained trees, which can bias the selection toward features with higher variance or more potential split points and may retain redundant information. Meanwhile, L1 regularization performs feature selection within a linear modeling framework by shrinking coefficients toward zero, which limits its ability to model nonlinear patterns or interactions among features. As a result, LGBM tends to select a feature subset that is both compact and highly informative, effectively filtering out noisy or redundant features while preserving strong predictive cues, as reflected by the improved classification accuracy achieved with a substantially reduced feature set. 

### _5.3.4. Effect of LGBM feature selection across deep architectures_ 

To provide a broader perspective, Table 12 shows the best-performing feature subsets obtained through LGBM-based selection across all evaluated deep architectures. A consistent trend emerges: for most models – Swin-Tiny, ConvNeXt-Base, DenseNet-121, and ResNet50 – the top 10% of selected features achieved the highest accuracy, outperforming the full feature sets. For instance, ConvNeXt-Base attained its best result (85.31%) with an SVM classifier using 103 features, indicating that LGBM effectively preserves nonlinear discriminative information. DenseNet-121 performed best with ET (83.60%), while ResNet-50 reached 83.49% with LGBM, reflecting robustness in moderately high-dimensional spaces. 

In contrast, EfficientNet-B0 deviates from the general trend, as its classification performance slightly decreased after feature selection (from 82.69% to 82.35%). This behavior can be attributed to its architecture, which is explicitly optimized for feature efficiency. Unlike ConvNeXt-Base or ResNet-50, which produce high-dimensional embeddings (1024 and 2048 features, respectively) with substantial redundancy, EfficientNet-B0 generates a compact 320-dimensional representation using compound scaling and MBConv blocks. As a result, the original feature space already contains limited noisy or irrelevant information. Further reducing this representation to 160 dimensions may therefore remove complementary discriminative cues, leading to a slight performance degradation. This observation suggests that posthoc feature selection is more effective for architectures with redundant representations, whereas compact backbones such as EfficientNet-B0 benefit less from aggressive dimensionality reduction. 

### _5.4. Computational complexity and efficiency analysis_ 

### _5.4.1. Analysis of model parameters and training time_ 

In addition to predictive accuracy, this study conducted an analysis of model complexity and computational cost, as illustrated in Fig. 7, to emphasize the trade-offs between different architectures. The findings 

indicate that parameter count is not the sole factor influencing computational expense; rather, architectural design plays a critical role in overall efficiency. To quantify this, we computed parameter efficiency as parameters (in millions) divided by training time per epoch (in seconds), which yielded units of M/s to measure processing speed. 

The comparison highlights the contrast between complexity and efficiency. ConvNeXt-Base (87.6M parameters, 89.0 s per epoch, efficiency ≈ 0.98 M/s) exemplifies a highly complex design that achieves strong accuracy but demands considerable resources, making it resource-intensive and potentially limiting its practicality for deployment on constrained hardware. In contrast, EfficientNet-B0 (4.1M parameters, 29.3 s per epoch, efficiency ≈ 0.14 M/s) represents the opposite extreme, offering remarkable efficiency at the cost of reduced accuracy. 

The classic architectures provide additional insight into these dynamics. DenseNet-121 (7.6M parameters, 39.1 s per epoch, efficiency ≈ 0.19 M/s) has far fewer parameters than ResNet-50 (23.6M parameters, 36.4 s per epoch, efficiency ≈ 0.65 M/s), yet it requires longer training time due to its feature concatenation operations. This outcome underscores that architectural choices, such as DenseNet’s dense connectivity, can outweigh raw parameter efficiency in terms of computational overhead. 

Within this context, Swin-Tiny emerged as the most balanced solution. With 27.5M parameters and a training time of 44.1 s per epoch (efficiency ≈ 0.62 M/s), it represents a moderate resource investment while achieving the highest accuracy among all models. It represented fewer computational resources than ConvNeXt-Base (about 31% fewer parameters and 50% less time per epoch), while still outperforming EfficientNet-B0 and DenseNet-121 in both accuracy and efficiency (e.g., 4.4 times higher than EfficientNet-B0’s 0.14 M/s), with only a modest increase in cost compared to ResNet-50. This combination of leading accuracy and manageable resource requirements identifies Swin-Tiny as the most compelling backbone for developing models that are both high-performing and practically deployable. 

Based on these observations, the analysis highlighted that model selection is a multi-dimensional decision involving more than predictive accuracy. While complex models like ConvNeXt-Base can achieve high accuracy and lightweight models like EfficientNet-B0 offer efficiency, neither extreme is optimal on its own. A balanced architecture such as Swin-Tiny provided a practical compromise, delivering state-of-the-art accuracy with manageable computational cost—particularly beneficial for applications in resource-limited environments like edge computing devices. This makes it suitable for further hybrid model development in real-world scenarios. 

### _5.4.2. Analysis of inference time_ 

Following the analysis of model parameters and training time, inference speed is a critical factor for evaluating the practical feasibility of a model, particularly for applications requiring rapid response or deployment on resource-constrained devices. In this study, we also analyze the inference time per image of the best-performing hybrid framework, which consists of deep feature extraction from Stage 4 of Swin-Tiny, followed by RF-based classification using the feature subset selected by LGBM. The detailed inference time results are reported in Table 13, which indicates that the total inference time per image is 17.878 ms. Notably, most of this time—specifically 17.865 ms, accounting for more than 99.9%–is spent on the deep feature extraction stage using the Swin-Tiny backbone. In contrast, the inference time of the RF classifier is only 0.013 ms, which is negligible. This result highlights the efficiency of the proposed hybrid approach. The feature selection using LGBM, which is performed offline during training, reduces the feature dimensionality from 768 to 77 compact features, enabling the RF classifier to produce predictions almost instantaneously. 

The inference-time analysis demonstrates that the proposed hybrid framework effectively balances strong feature representation and fast prediction, making it suitable for real-time deployment in automated aquatic product quality monitoring systems. 

12 



<!-- Start of picture text -->
87.6m 22-08 mmm Parameters (Millions)<br>jem Time per Epoch (seconds)<br>80 - 80<br>a<br>@ 604 +60 2<br>268%<br>Z 2<br>: 5<br>8 44.18 Q<br>o Ww<br>5 40 J 39.15 ede L4Q 40 S<br>& E<br>27.5M 29.35 fa<br>23.6M<br>205 720<br>7.6M<br>0! | | Lo<br>ConvNeXt-Base Swin-Tiny EfficientNet-BO DenseNet-121 ResNet-50<br><!-- End of picture text -->



<!-- Start of picture text -->
90<br>Methods<br>fmm Hybrid DL-ML (Optimized Features)<br>85.99% 85.88% , jm Hybrid DL-ML (Full Features)<br>85 et mmm Deep Learning Model<br>mmm Handcrafted Features(Hoang et al., 2025)<br>mem MB-BE (Yildiz et al., 2024)<br>mmm =VGG19 + ANN (Prasetyo et al., 2022)<br>80<br>77.56% 77.30%<br>=<br>Bas<br>3<br>8<br><<br>70<br>65<br>63.21%<br>0 L |<br><!-- End of picture text -->



<!-- Start of picture text -->
Highly Fresh Fresh Not Fresh<br>EE |<br>2 =<br>o<br>vo 3 Pi ; i j<br>~~ 8 3<br>— oe<br>—<br>ov > ny -<br>(oS on Ae<br>2 y<br>— 2<br>S 2<br>|hm<br>3 5<br>S$72)<br><!-- End of picture text -->

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 

rigorous assessment of its robustness and generalization potential under varying lighting conditions, fish species, and acquisition environments. Finally, further optimization for low-latency deployment, including integration into mobile or embedded systems, represents a promising avenue for supporting time-sensitive and real-time seafood quality inspection applications. 

### **6. Conclusion** 

This study introduced a unified three-stage framework for optimizing deep visual representations in fish eye freshness assessment on the challenging FFE dataset. By fine-tuning state-of-the-art vision backbones, extracting multi-level features, applying classical ML classifiers, and performing embedded feature selection, the best configuration– Swin-Tiny features combined with an RF classifier and LGBM-based selection achieved an accuracy of 85.99%, outperforming prior studies on the same dataset by 8.69–22.78%. The results highlight the effectiveness of integrating vision transformers with boosting-based feature optimization for improved accuracy, interpretability, and efficiency in visual food quality tasks. Practically, this approach offers a scalable, objective tool for near real-time quality control in the seafood industry, helping minimize economic losses and enhance food safety. While limited by the FFE dataset’s specific characteristics (e.g., eight species and uncontrolled mobile imaging), the flexible framework is generalizable to broader food imaging applications. Future work will validate it on diverse datasets, explore multimodal integration, and develop lightweight models for mobile deployment. 

### **CRediT authorship contribution statement** 

**Phi-Hung Hoang:** Writing – review & editing, Writing – original draft, Visualization, Software, Methodology, Formal analysis, Data curation, Conceptualization. **Nam-Thuan Trinh:** Writing – original draft, Visualization, Software, Methodology, Investigation, Formal analysis, Data curation. **Van-Manh Tran:** Writing – original draft, Visualization, Software, Methodology, Investigation, Formal analysis, Data curation. **Thi-Thu-Hong Phan:** Writing – review & editing, Writing – original draft, Validation, Supervision, Project administration, Methodology, Formal analysis, Conceptualization. 

### **Declaration of Generative AI and AI-assisted technologies in the writing process** 

During the preparation of this manuscript, Grammarly and generative large language models were employed to improve grammar and refine wording for clarity. The authors subsequently reviewed and revised the content as necessary and take full responsibility for the final version of the manuscript. 

### **Funding** 

This research received no funding. 

### **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

### **Data availability** 

The dataset used in this study is available in the Mendeley Data repository (Prasetyo et al., 2022a). 

The source code is available at GitHub Repository. 

### **References** 

Arora, M., Mangipudi, P., Dutta, M.K., 2022. A low-cost imaging framework for freshness evaluation from multifocal fish tissues. J. Food Eng. 314, 110777. http: //dx.doi.org/10.1016/j.jfoodeng.2021.110777. 

- Balım, C., Olgun, N., Çalışan, M., 2025. Leveraging feature fusion of image features and laser reflectance for automated fish freshness classification. Sensors 25 (14), http://dx.doi.org/10.3390/s25144374. 

- Biswas, S., Nahata, C., Ghosh, S., Sahoo, S., Biswas, D., 2025. Fish freshness detection via hybrid CNN-LSTM: An interpretable deep learning model. In: Dehuri, S., Dash, S., Thulasiram, R.K., Singh, R.H., Favorskaya, M. (Eds.), Biologically Inspired Techniques in Many Criteria Decision-Making. Springer Nature Switzerland, Cham, pp. 365–373. http://dx.doi.org/10.1007/978-3-031-82706-8_37. 

- Breiman, L., 2001. Random forests. Mach. Learn. 45, 5–32. 

- Cahyo, N.R.D., Al-Ghiffary, M.M.I., 2024. An image processing study: Image enhancement, image segmentation, and image classification using milkfish freshness images. Int. J. Eng. Comput. Adv. Res. (IJECAR) 1 (1), 11–22. 

- Chen, J., Jayachandran, M., Bai, W., Xu, B., 2022. A critical review on the health benefits of fish consumption and its bioactive constituents. Food Chem. 369, 130874. http://dx.doi.org/10.1016/j.foodchem.2021.130874. 

- Cortes, C., Vapnik, V., 1995. Support-vector networks. Mach. Learn. 20 (3), 273–297. Dorogush, A.V., Ershov, V., Gulin, A., 2018. CatBoost: gradient boosting with categorical features support. CoRR arXiv:1810.11363. 

- Fix, E., Hodges, J., 1951. Discriminatory analysis, nonparametric discrimination: Consistency properties. Technical Report 4, USAF School of Aviation Medicine, Randolph Field, USA. 

- Geurts, P., Ernst, D., Wehenkel, L., 2006. Extremely randomized trees. Mach. Learn. 63 (1), 3–42. 

- Hardy, M., Kashani Zadeh, H., Tzouchas, A., Vasefi, F., MacKinnon, N., Bearman, G., Sokolov, Y., Haughey, S.A., Elliott, C.T., 2024. Freshness in salmon by handheld devices: Methods in feature selection and data fusion for spectroscopy. ACS Food Sci. Technol. 4 (12), 2813–2823. http://dx.doi.org/10.1021/acsfoodscitech. 4c00331. 

- Hassoun, A., Karoui, R., 2017. Quality evaluation of fish and other seafood by traditional and nondestructive instrumental methods: Advantages and limitations. Crit. Rev. Food Sci. Nutr. 57 (9), 1976–1998. http://dx.doi.org/10.1080/10408398. 2015.1047926, PMID: 26192079. 

- He, K., Zhang, X., Ren, S., Sun, J., 2016. Deep residual learning for image recognition. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. CVPR. 

- Hoang, P.H., Trinh, N.T., Tran, V.M., Phan, T.T.H., 2026. Enhanced fish freshness classification with incremental handcrafted feature fusion. URL https://arxiv.org/ abs/2510.17145 arXiv:2510.17145. 

- Hosmer, D.W., Lemeshow, S., 2000. Introduction to the logistic regression model. In: Applied Logistic Regression. John Wiley & Sons, New York, pp. 1–30. 

- Huang, G., Liu, Z., van der Maaten, L., Weinberger, K.Q., 2017. Densely connected convolutional networks. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 

- Jayasundara, J., Ramanayake, R., Senarath, H., Herath, H., Godaliyadda, G., Ekanayake, M., Herath, H., Ariyawansa, S., 2023. Deep learning for automated fish grading. J. Agric. Food Res. 14, 100711. http://dx.doi.org/10.1016/j.jafr.2023. 100711. 

- Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., Liu, T.-Y., 2017. Lightgbm: A highly efficient gradient boosting decision tree. In: Proceedings of the 31st Conference on Neural Information Processing Systems (NIPS 2017). Long Beach, CA, USA, pp. 3149–3157. 

- Khaleel, Y.L., Habeeb, M.A., Shayea, G.G., 2024. Integrating image data fusion and ResNet method for accurate fish freshness classification. Iraqi J. Comput. Sci. Math. 5 (4), 21. http://dx.doi.org/10.52866/2788-7421.1226. 

- Kılıçarslan, S., Çiçekliyurt, M., Kılıçarslan, S., 2024. Fish freshness detection through artificial intelligence approaches: A comprehensive study. Turk. J. Agric. - Food Sci. Technol. 12, 290–295. http://dx.doi.org/10.24925/turjaf.v12i2.290-295.6670. 

- Lanjewar, M.G., Panchbhai, K.G., 2024. Enhancing fish freshness prediction using NasNet-LSTM. J. Food Comp. Anal. 127, 105945. http://dx.doi.org/10.1016/j.jfca. 2023.105945. 

- Lap, B.Q., Phan, T.T.H., Nguyen, H.D., Quang, L.X., Hang, P.T., Phi, N.Q., Hoang, V.T., Linh, P.G., Hang, B.T.T., 2023. Predicting water quality index (WQI) by feature selection and machine learning: A case study of an kim hai irrigation system. Ecol. Informatics 74, 101991. http://dx.doi.org/10.1016/j.ecoinf.2023.101991. 

- Liu, Z., Lin, Y., Cao, Y., Hu, H., Wei, Y., Zhang, Z., Lin, S., Guo, B., 2021. Swin transformer: Hierarchical vision transformer using shifted windows. In: 2021 IEEE/CVF International Conference on Computer Vision. ICCV, pp. 9992–10002. 

- Liu, Z., Mao, H., Wu, C.Y., Feichtenhofer, C., Darrell, T., Xie, S., 2022. A ConvNet for the 2020s. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 

- McCulloch, W., Pitts, W., 1943. A logical calculus of the ideas immanent in nervous activity. Bull. Math. Biophys. 5, 115–133. 

- Medeiros, E.C., Almeida, L.M., Filho, J.G.d.A.T., 2021. Computer vision and machine learning for tuna and salmon meat classification. Informatics 8 (4), http://dx.doi. org/10.3390/informatics8040070. 

15 

_P.-H. Hoang et al._ 

_Ecological Informatics 95 (2026) 103711_ 

Peries, R.F.S., Adeeba, S., Ahamed, M.S., Kumara, B., 2025. AI-driven solutions for automated fish freshness classification using CNN architectures. In: 2025 International Research Conference on Smart Computing and Systems Engineering. SCSE, pp. 1–6. http://dx.doi.org/10.1109/SCSE65633.2025.11031016. 

- Phan, T.-T.-H., Nguyen, L.H.B., 2025. Enhancing rice seed purity recognition accuracy based on optimal feature selection. Ecol. Informatics 86, 103044. http://dx.doi. org/10.1016/j.ecoinf.2025.103044. 

- Prabhakar, P.K., Vatsa, S., Srivastav, P.P., Pathak, S.S., 2020. A comprehensive review on freshness of fish and assessment: Analytical methods and recent innovations. Food Res. Int. 133, 109157. http://dx.doi.org/10.1016/j.foodres.2020.109157. 

- Prasetyo, E., Adityo, R.D., Suciati, N., Fatichah, C., 2022a. The freshness of the fish eyes dataset. http://dx.doi.org/10.17632/xzyx7pbr3w.1, Mendeley Data, V1. 

- Prasetyo, E., Purbaningtyas, R., Adityo, R.D., Suciati, N., Fatichah, C., 2022b. Combining MobileNetV1 and depthwise separable convolution bottleneck with expansion for classifying the freshness of fish eyes. Inf. Process. Agric. 9 (4), 485–496. http://dx.doi.org/10.1016/j.inpa.2022.01.002. 

- Rodrigues, J.P., Pacheco, O.R., Correia, P.L., 2024. Seabream freshness classification using vision transformers. In: Vasconcelos, V., Domingues, I., Paredes, S. (Eds.), Progress in Pattern Recognition, Image Analysis, Computer Vision, and Applications. Springer Nature Switzerland, Cham, pp. 510–525. 

- Sanga, H., Saka, P., Nanded, M., Alpuri, K.N., Nadella, S., 2024. Tilapia fish freshness detection using CNN models. In: Garg, D., Rodrigues, J.J.P.C., Gupta, S.K., Cheng, X., Sarao, P., Patel, G.S. (Eds.), Advanced Computing. Springer Nature Switzerland, Cham, pp. 67–80. 

- Selvaraju, R.R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., Batra, D., 2017. GradCAM: Visual explanations from deep networks via gradient-based localization. In: 2017 IEEE International Conference on Computer Vision. ICCV, pp. 618–626. 

- Syarwani, M., Nugraha, G., Dwiyansaputra, R., Khairunnas, K., 2022. Classification of nile tilapia’s freshness based on eyes and gills using support vector machine. pp. 156–168. http://dx.doi.org/10.2991/978-94-6463-084-8_15. 

- Tan, M., Le, Q.V., 2020. EfficientNet: Rethinking model scaling for convolutional neural networks. URL https://arxiv.org/abs/1905.11946 arXiv:1905.11946. 

- Tidwell, J.H., Allan, G.L., 2001. Fish as food: aquaculture’s contribution. Ecological and economic impacts and contributions of fish farming and capture fisheries. EMBO Rep. 2 (11), 958–963. http://dx.doi.org/10.1093/embo-reports/kve236. 

- Yildiz, M.B., Yasin, E., Koklu, M., 2024. Fisheye freshness detection using common deep learning algorithms and machine learning methods with a developed mobile application. Eur. Food Res. Technol. 250, 1–14. http://dx.doi.org/10.1007/s00217024-04493-0. 

16 

