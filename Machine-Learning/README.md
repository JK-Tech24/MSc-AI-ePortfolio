<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My ePortfolio</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body {
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                background-color: #f8f9fa; /* Light gray-blue */
            }
            
            header {
                background-color: #1e3a8a; /* Dark blue */
                color: white;
                padding: 20px;
                text-align: center;
            }
            
            nav {
                display: flex;
                justify-content: center;
                gap: 15px;
                margin: 15px 0;
            }
            
            nav a {
                color: white;
                text-decoration: none;
                font-size: 18px;
                font-weight: bold;
            }
            
            nav a:hover {
                text-decoration: underline;
            }
            
            .container {
                display: flex;
            }
            
            .sidebar {
                width: 25%;
                background-color: #121212; /* Dark gray */
                color: #e0e0e0; /* Light gray */
                height: 100vh;
                padding: 15px;
                overflow-y: auto;
            }
            
            .sidebar h3 {
                text-align: center;
                margin-bottom: 20px;
                color: #00897b; /* Teal */
            }
            
            .sidebar ul {
                list-style-type: none;
                padding: 0;
            }
            
            .sidebar ul li {
                margin-bottom: 10px;
            }
            
            .sidebar ul li a {
                color: #e0e0e0; /* Light gray */
                text-decoration: none;
                font-size: 16px;
            }
            
            .sidebar ul li a:hover {
                text-decoration: underline;
            }
            
            .content {
                width: 75%;
                padding: 20px;
                overflow-y: auto;
            }
            
            .card {
                background-color: #ffffff; /* White */
                margin: 15px 0;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .card h3 {
                margin-top: 0;
                color: #1e3a8a; /* Dark blue */
            }
            
            .card p {
                font-size: 14px;
                color: #555; /* Subtle gray for text */
            }
            
            .card a {
                display: inline-block;
                background-color: #00897b; /* Teal */
                color: white;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 10px;
            }
            
            .card a:hover {
                background-color: #005f56; /* Darker teal */
            }
            
            .slider {
                display: flex;
                gap: 15px;
                margin: 20px 0;
                overflow-x: auto;
            }
            
            .slider img {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                border: 2px solid #00897b; /* Teal */
            }
            
            
        
        
        
        
        }
       
            #education {
    margin-left: 0; /* Adjust as needed to align with other elements */
}

.education-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start; /* Aligns items to the left */
}

.education-card {
    margin-bottom: 15px; /* Adjust for spacing between cards */
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

    #education {
        padding: 2rem;
        background-color: #f9f9f9;
        color: #333;
        text-align: center;
    }
    .education-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 1rem;
    }
    .education-card {
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        padding: 1.5rem;
        width: 300px;
        text-align: left;
        transition: transform 0.3s ease;
    }
    .education-card:hover {
        transform: translateY(-10px);
    }
    .education-card h3 {
        color: #2a7de1;
        margin-bottom: 0.5rem;
    }
    .education-card h4 {
        font-weight: 400;
        margin-bottom: 0.5rem;
    }
    .education-card p {
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
        line-height: 1.4;
    }


   
    .card {
        background: #ffffff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
    }
    .card h3 {
        color: #d5ac19;
        margin-bottom: 15px;
    }
    .card p {
        margin-bottom: 15px;
    }
    .card ul {
        margin: 10px 0;
        padding-left: 20px;
    }
    .card ul li {
        margin-bottom: 5px;
    }
    .artifact-link {
        display: inline-block;
        margin-top: 15px;
        padding: 10px 15px;
        color: #fff;
        background-color: #d5ac19;
        text-decoration: none;
        border-radius: 4px;
    }
    .artifact-link:hover {
        background-color: #d5ac19;
    }
    /* Footer Section Styles */
#footer {
    background-color: #333;
    color: #fff;
    padding: 20px;
    text-align: left;
}

.footer-container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}

.footer-content {
    flex: 1;
    margin: 10px;
}

.footer-content h4 {
    margin-bottom: 10px;
    font-size: 1.2em;
}

.footer-content p, .footer-content ul {
    font-size: 1em;
}

.social-links {
    list-style: none;
    padding: 0;
}

.social-links li {
    margin: 5px 0;
}

.social-links a {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s;
}

.social-links a:hover {
    color: #1e90ff;
}

.footer-bottom {
    text-align: center;
    margin-top: 20px;
    font-size: 0.9em;
}

</style>
    </style>
</head>
<body>
    <header>
        <h1>Welcome to My e-Portfolio</h1>
        <nav>
            <a href="#about">About</a>
            <a href="#skills">Skills</a>
            <a href="#work">Formative and e-Portfolio Activities (project units)</a>
            <a href="#contact">Contact</a>
        </nav>
    </header>
    

    <div class="container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <h3>Table of Contents</h3>
            <ul>
                <li><a href="#about">About</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#work">Formative and e-Portfolio Activities (project units)</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </aside>

        <!-- Content -->
        <main class="content">
            <!-- About Section -->
            <section id="about">
                <h2>About Me</h2>
                <p>I’m Jaafar El-Komati, an MSc student in Artificial Intelligence at the University of Essex. This is my e-portfolio for the Machine Learning module (October 2024).</p>
            </section>

            <!-- Skills Section -->
            <section id="skills">
                <h2>Skills Gained</h2>
                <ul>
                    <li>Python</li>
                    <li>CNNs, Statistical Analysis, Machine Learning</li>
                    <li>GitHub</li>
                    <li>Reflective Writing, Critical Analysis</li>
                    <li>Google Colab</li>
                </ul>
            </section>

            <!-- Work Per Unit Section -->
            <section id="work">
                <h2>Formative and e-Portfolio Activities (project units)</h2>
                <div class="card">
                    <h3>Unit 1: Collaborative Discussion</h3>
                  
                    <p>
                        <strong>Initial Post</strong><br>
                        In my initial post, I discussed the 2015 IT crash at the Royal Bank of Scotland (RBS), which led to the loss of 600,000 customer payments. This incident underscores the significant challenges that information system failures can have in the banking sector in the era of Industry 4.0, where the convergence of technology blurs the boundaries between physical, digital, and biological domains with information systems playing a central role (Schwab, 2016). The impact on affected customers included financial difficulties due to delayed wages, tax credits and other benefits, emphasizing the crucial role banks play in maintaining reliable systems (Peachey, 2015).                    </p>
                    <a href="https://colab.research.google.com/drive/1ovmf3o8S_ZAf_2XbVGIxNlXCHj0HvlEq?usp=sharing" target="_blank">View Artifact</a>

                    <p>
                        <strong>Peer Response, Guilherme Pessoa-Amorim</strong><br>
                        In response to my post, Guilherme pointed out the necessity for strong information systems in light of increasing cyber threats in the banking industry. He noted that organizations need to focus on IT integrity and security through regular updates and thorough regulatory oversight given the managing of large volumes of financial transactions requiring the implementation of backup systems (Mathias et al., 2024; Verma, 2024).                    </p>
                    <a href="https://colab.research.google.com/drive/1HAlr_9NjeQk9_NsraH_hVsRcAp-yxQey" target="_blank">View Artifact</a>

                    <p>
                        <p>
                            <strong>Peer Response, by Georgios Papachristou</strong><br>
                            Georgios contributed to this discussion by addressing the systemic cyber risks present in the financial ecosystem, referencing incidents like the Knight Capital Group's coding error that disrupted trading worth $28 trillion of stock in the New York Stock Exchange (Kello, 2017). He highlighted the importance of being prepared and having backup plans backup plan to temporarily disable the digitalized part of the financial system if needed can help contain risks and ensure stability.</p>
                           
                     <a href="https://colab.research.google.com/drive/1hCrAKD6X75nLRwqGJObrTxuiBaRnvsVF?usp=sharing" target="_blank">View Artifact</a>
    
                        <p>

                        <strong>Summary Post</strong><br>
                        Together, these discussions emphasize that as the banking sector continues to adopt digitalization, the ramifications of information system failures can be significant, impacting consumers, institutions, and the broader economy. Therefore, investing in modern, resilient technology and proactive regulatory measures is essential to avoid similar incidents in the future enabling banks to effectively protect their operations and their customers' interests in a complex digital environment.                    </p>
                    <a href="https://colab.research.google.com/drive/1an_8GuceQaXcsL6_k5-Uy8ZHMgQjTxhu?usp=sharing" target="_blank">View Artifact</a>
                </div>
                
                
                <div class="card">
                    <h3>Unit 2: Seminar Preparation</h3>
                    <p>
                   
                    <p>For my seminar preparation, I conducted an Exploratory Data Analysis (EDA) of the Auto-mpg dataset using Python on Google Colab. I started by identifying and addressing any missing values in the dataset.  Subsequently, I checked for skewness and kurtosis in order to understand more about the distribution of the data set that I took. I then used a correlation heat map to bring out relations of different features of the data set so as to determine if there where any dependencies. For the actual analysis of these relationships, I created pairplots to investigate bivariate coefficients between every two variables. The outlined EDA procedure gave me an opportunity to discover properties of the dataset and get ready for further analysis.</p>
                    <a href="https://colab.research.google.com/drive/1kOf5vCPlM3jHplXVqjc5g2m0lGeEiPdS" target="_blank">View Artifact</a>
                </div>
                
                <!-- Unit 2 -->
                <div class="card">
                    <h3>Unit 3: E-Portfolio Component</h3>
                    <p>For this component, I analyzed the correlation and regression and, thereby, download and uploaded a few notebooks to Google Colab appropriately. I altered the variable of the data points within the code to determine the impact made to the correlation and regression results.
                        The notebooks (artifacts) include my analysis and modifications, with detailed comments throughout:
                        </p>
                        <p>Covariance Pearson Correlation artifact:
                            </p>
                    <a href="https://colab.research.google.com/drive/17rATz8dGtHINWNewQK-ynpGpuO7r_ipY" target="_blank">View Artifact</a>
                    <p> Linear Regression artifact:
                    </p>
                    <a href="https://colab.research.google.com/drive/1cHFigmOaFzdpjIKpMydOo0ltDMobTjOS" target="_blank">View Artifact</a>
                    <p> Multiple linear regression:
                    </p>
                    <a href="https://colab.research.google.com/drive/15ukfT3eJiAzLI-Zx4zqXZfAEQgI18RGz" target="_blank">View Artifact</a>
                    <p> Polynomial regression:
                    </p>
                    <a href="https://colab.research.google.com/drive/1pGrJpAWYXxdtUoWs5dwRzgg4J6xdb7hi" target="_blank">View Artifact</a>
                
                </div>
                
                <!-- Unit 2 -->
                <div class="card">
                    <h3>Unit 4:</h3>
                  
                    <strong>Task A: Correlation Analysis</strong><br>
                    <p>I analyzed the correlation between the mean population and mean per capita GDP for countries from 2001 to 2021. To reach my conclusions, I judged from the preprocessed data and then embarked on logarithmic transformations and looked for the Pearson correlation coefficient. This was further revealed in the study where there was an inverse relationship between population and per capita GDP, meaning that in as far as population is concerned, per capita GDP reduces.</p>
                    <a href="https://colab.research.google.com/drive/14koJQTTNAdmE00CFvWzZLDPeCcjPqmlH" target="_blank">View Artifact</a>
               
                  
                   
                    <p>
                        <strong>Task B: Linear Regression</strong><br>
                        In Task B using linear regression for the population mean as the predictor and mean per capita GDP as the response. Because of the variability of the values, logarithmic transformations were adopted in the process. The results showed a regression model with population size and per capita GDP of the selected countries in the year 2001-2021.</p>
                    <a href="https://colab.research.google.com/drive/1WnCuMdZt1aBlYRV3HG_nbpA9A1AoPopT" target="_blank">View Artifact</a>
                </div>
                
                <!-- Unit 2 -->
                <div class="card">
                    <h3>Unit 5: Wiki Activity</h3>
                    <strong>Wiki Activity: Clustering</strong><br>
                    <p>In this activity I learned about clustering and the K-Means algorithm using a live animation that illustrates how data is classified and what the clusters look like. I used a heuristic process of assigning clusters without pre-acquainted knowledge of the clusters; I initialized random centroids on the feature space, and then used a nearest neighbour approach to assign data points to clusters, recalculating the centroids until the cluster representation became stable. What became clear in this process watched through detecting values through interactive learning was that the K-Means algorithm groups information without outcomes attached to them.</p>
                    <a href="https://colab.research.google.com/drive/1dgL4pES3P5iWNSFTWgQK5jIwSRy7ZtMr?usp=sharing" target="_blank">View Artifact</a>
                    <p></p>
                    <strong>e-Portfolio Activity: Jaccard Coefficient Calculations</strong><br>
                    <p>Calculate Jaccard coefficient for the following pairs:
                        (Jack, Mary)
                        (Jack, Jim)
                        (Jim, Mary)
                        </p>
                    <a href="https://colab.research.google.com/drive/1yCMZRD87l1n31CH_AAn4lpwSsHKBG1Dr" target="_blank">View Artifact</a>
                </div>
                <!-- Unit 2 -->
                <div class="card">
                    <h3>Unit 6:</h3>
                    <strong>Team's progress</strong><br>
                    This documentation outlines the team's progress, including pre-meeting preparations, key discussions during the first and second meetings, and the distribution of tasks. Highlights include the creation of a team contract, a business questions table, and the analysis plan focused on Airbnb pricing factors. Tasks were assigned to team members for completion within specified deadlines.
                </p>
                <a href="https://colab.research.google.com/drive/145_6kPLxImyGgHy4by-3XzjGdxndaZPS?usp=sharing" target="_blank" class="artifact-link">View Artifact</a>
                </p>
                <strong>Team's project analysis</strong><br>
                <a href="https://colab.research.google.com/drive/1jcrnzhAlQrXVF1PEFIfNpsysSveYkUS2" target="_blank" class="artifact-link">View Artifact</a>
                </p>
                <strong>Seminar Preparation</strong><br>
                          <strong>Task A</strong><br>
                    <p>In particular, I applied K-Means clustering on the Iris dataset, after which I reindexed clusters according to the species: In the table below, I computed the confusion matrix to evaluate the clustering accuracy of the dataset; K-Means clustering accuracy in the present case was 57.33%. Comparing the setosa species with the other two classes, it classified all virginica species correctly while misclassifying some of the setosa and versicolor species due to very close feature space for these two classes. </p>
                    <a href="https://colab.research.google.com/drive/1KseRpgzR_5o_D26SG1CPVdvxYEeMClag" target="_blank">View Artifact</a>
                
                  
                    <p>  <strong>Task B</strong><br>
                        In Task B, I analyzed the Wine dataset in which I had to use K-Means clustering to cluster wines by their features. The work was six parts: data preprocessing, making K-Means algorithm, visualizing the clusters, and calculating the basic criteria on the model.</p>
                    <a href="https://colab.research.google.com/drive/1stiWIgf0-c5OrutW9n5DLip1FIINry5j" target="_blank">View Artifact</a>
                </div>
                <!-- Unit 2 -->
                <div class="card">
                    <h3>Unit 7: 
                        e-Portfolio Activity: Perceptron Activities</h3>
                    <p>This code is a basic perceptron via NumPy in which I defined functions for activation, predict, and training it. This enables the perceptron to make further learning from inputs and desired outputs enabling it to maximize on patterns it takes as a basis of its classifications.</p>
                    <strong>simple perceptron</strong><br>
                </p>
                    
                    <a href="https://colab.research.google.com/drive/1-0Ql1G1h2IJxd42FO_zSpFM0Fa4G6d-0" target="_blank">View Artifact</a>
                    </p>    
                    <strong>Perceptron AND operator</strong><br>
                    </p> 
                    <a href="https://colab.research.google.com/drive/1Ichfa-RFuy0EIiVmZDJxglc-eIaw4TPa" target="_blank">View Artifact</a>
                    </p>
                    <strong>Multi layer Perceptron</strong><br>
                    </p>
                        <a href="https://colab.research.google.com/drive/1_23srrvMPiDIqxbi-5JPDv_aXKYSalB1#scrollTo=TJnppXrtTvKl" target="_blank">View Artifact</a>
                    </p>


          </div>
                <div class="card">
                    <h3>Unit 8: Training an Artificial Neural Network</h3>
                    <strong>Emerging Research in ANN</strong><br>
                    <p>
                        This unit explores the transformative impact of Artificial Neural Networks (ANN) on the healthcare sector, particularly in enhancing diagnostic accuracy and personalized treatment. It highlights the need for rigorous testing and ethical considerations to ensure fairness and mitigate biases in medical applications.
                    </p>
                    <a href="https://colab.research.google.com/drive/1jHjnimnWM_QLMPRiuyX5cDErZLkQQpRJ" target="_blank" class="artifact-link">View Artifact</a>
                    </p>
                    <strong>Gradient Cost Function</strong><br>
                    </p>
                    <p>By increasing the iterations from 100 to 500 and reducing the learning rate from 0.08 to 0.01, the algorithm took more time to converge but achieved a lower total cost, preventing overshooting and improving the accuracy of the regression model.</p>
                    <a href="https://colab.research.google.com/drive/1SSBJnJbtWPMev8Uk58auusrDykxAqYDb#scrollTo=_LAsza2RirQL" target="_blank">View Artifact</a>
                </div>
                <div class="card">
                    <h3>Unit 8-10:Collaborative Discussion 2</h3>
                    <strong>Initial Post</strong><br>
                   </p>
                    <a href="https://colab.research.google.com/drive/1tlSKOaOh2sYYEijebj1Xa_Oj9KJCpQub?usp=sharing" target="_blank">View Artifact</a>
                   </p>
                    <strong>Peer Response, Ben Zapka </strong><br>
                   </p>
                    <a href="https://colab.research.google.com/drive/1NU9eLTjOKBxZZXE0eq_VAzC_3y0Ugx72" target="_blank">View Artifact</a>
                   </p>
                    <strong>Peer Response, Khadijah Harding  </strong><br>
                   </p>
                    <a href="https://colab.research.google.com/drive/1ZgeRhF-ho_8MGZaKvn2BikDmJRoRH-H0#scrollTo=zpZmzB_uE1rG" target="_blank">View Artifact</a>
                   </p>
                    <strong>Summary Post</strong><br>
                   </p>
                    <a href="https://colab.research.google.com/drive/1rptT1ouzb6QOcGrzN4g62INaxdPCK6Nz" target="_blank">View Artifact</a>
                   </p>


                </div>
                <div class="card">
                    <h3>Unit 9:E-Portfolio Component</h3>
                    <p>This project involved developing a convex CNN for object recognition using TensorFlow or Keras. I modified the input image for prediction, changing the index from 16 to 5 to predict that the 6th image is a 'frog'. This demonstrates how CNNs are used in computer vision for object identification. However, ethical concerns such as privacy, surveillance, and bias in AI models highlight the need for regulation to ensure legal, non-biased, and user-friendly AI, especially in sensitive fields like security and healthcare (Wall, 2019).</p>
                    <a href="https://colab.research.google.com/drive/1zvJhoEqn1O9jkdPTSkg1G4yX2uf7Gzv3" target="_blank">View Artifact</a>
                </div>
                <div class="card">
                    <h3>Unit 10:Seminar Preparation</h3>
                    <p>In this activity, I explored image classification with a CNN trained on the CIFAR-10 dataset, which performed well on training data and correctly identified a 'car,' but misclassified a 'teacup' as a 'frog,' highlighting CNN's ability to learn features like edges and textures while struggling with unfamiliar objects, demonstrating their utility in image classification and limitations with unseen categories.</p>
                    <a href="https://colab.research.google.com/drive/1j3qWIpczUNEzXYgCQjlz0-aSxo9beVPh" target="_blank">View Artifact</a>
                </div>
                <div class="card">
                    <h3>Unit 11: e-Portfolio Component</h3>
                    <p>I explored how different parameters affected AUC and R² error by applying Logistic Regression for classification and Linear Regression for regression, using the breast cancer dataset and a synthetic dataset, respectively, demonstrating the impact of regularization penalties and iterations on model performance and emphasizing the importance of fine-tuning parameters for optimal results.</p>
                    <a href="https://colab.research.google.com/drive/1dlfGgI1s4kS6brleXFSd8P_bFQ0Cq8GM?usp=sharing" target="_blank">View Artifact</a>
                </div>
                <div class="card">
                    <h3>Unit 12: 
                    <p> 
                    <strong>Future of Machine Learning</strong><br>
                    <a href="https://colab.research.google.com/drive/1IGcq9OomG-tO4dQGrTdIBII0ulISCG51#scrollTo=tQ_ufk7KXpg7" target="_blank">View Artifact</a>
                    <p> 
                    <strong>Reflective Summary</strong><br>
                    <a href="https://docs.google.com/document/d/1h94BL99Rh6SJRy6OKWiNG7iIRCQw62toHnlXxtUxPGM/edit?tab=t.0" target="_blank">View Summary</a>
                    <p>
                </div>
            </section>
<!-- Education Section -->
<section id="education">
   
    <div class="education-container">
        <h2>Education</h2>
        <!-- Education Card 1 -->
        <div class="education-card">
            <h3>Bachelor of Architectural Engineering</h3>
            <h4>Beirut Arab University, Lebanon</h4>
            <p><strong>Sept 2003 – June 2008</strong></p>
        </div>

        <!-- Education Card 2 -->
        <div class="education-card">
            <h3>Master of Science in Construction Project Management</h3>
            <h4>University of Manchester, UK</h4>
            <p><strong>Sept 2008 – Sept 2009</strong></p>
        </div>

        <!-- Education Card 3 -->
        <div class="education-card">
            <h3>Master of Science in Artificial Intelligence (AI)</h3>
            <h4>University of Essex, UK</h4>
            <p><strong>April 2024 – present</strong></p>
        </div>
<!-- Contact Section -->
    
<div class="container">
    <!-- Other sections -->

    <!-- Contact Section -->
    <div id="contact" class="education-container">
        <h2>Contact</h2>
        <div class="education-card">
            <p>LinkedIn: <a href="https://lb.linkedin.com/in/jaafar-el-komati">jaafar-el-komati</a></p>
            <p>Phone: +9613965665</p>
            <p>Lebanon</p>
        </div>
    </div>
</div>

            </section>
        </main>
    </div>
</body>
<!-- Footer Section -->
<footer id="footer">
    <div class="footer-container">
        <div class="footer-content">
            <h4>Contact Information</h4>
            <p>Phone: +9613965665 (Lebanon)</a></p>
        </div>
        <div class="footer-content">
            <h4>Follow Me</h4>
            <ul class="social-links">
                <li><a href="https://www.linkedin.com/in/jaafar-el-komati/" target="_blank">LinkedIn</a></li>
               
            </ul>
        </div>
        <div class="footer-content">
            <h4>About This Portfolio</h4>
            <p>This ePortfolio showcases my professional journey, skills, projects, and achievements in Msc Artificial Intelligence.</p>
        </div>
    </div>
    <div class="footer-bottom">
        <p>&copy; 2024 Jaafar El-Komati. All rights reserved.</p>
    </div>
</footer>

</html>


