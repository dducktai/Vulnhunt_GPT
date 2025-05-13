# VulnHunt-GPT: A Smart Contract Vulnerabilities Detector

VulnHunt-GPT leverages the power of OpenAI's ChatGPT to detect vulnerabilities in Solidity-based smart contracts. By combining advanced language models with static analysis techniques, this tool provides an innovative approach to enhancing the security of decentralized applications (DApps).

## Features

- **Automated Vulnerability Detection**: Detect common vulnerabilities in Solidity smart contracts, such as reentrancy attacks, integer overflows/underflows, and time manipulation,...
- **Use Pinecone as vector database**: cloud vector database, allowing admins to see the metrics, leading to a more manageable environment
- **Use Langchain to build LLM**: numerous convienient methods
- **Learn from your dataset**
- **OpenAI GPT Integration**: Leverages natural language processing to identify patterns and potential risks in smart contract code.
- **User-Friendly Interface**: Supports intuitive input methods for Solidity contracts and detailed vulnerability reports.

## Installation

To set up VulnHunt-GPT locally, follow these steps:

### Prerequisites
- Python 3.9 or later
- OpenAI API key, Gemini API key, Pinecone API key

## Usage

1. **Input the Solidity code**: Provide the source code of your Solidity contract.
2. **Analysis**: The tool uses GPT to analyze the code for vulnerabilities.
3. **Output**: View a detailed report highlighting vulnerabilities, remediations.

## Example

for CLI: python query.py
for GUI: streamlit run GUI_final.py

Output:
```
Detected vulnerabilities:
- Vulnerabilities: Reentrancy vulnerability X function 
- Recommendation: Use checks-effects-interactions pattern.
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- OpenAI for providing the GPT model.
- Solidity developers and the blockchain security community for insights on common vulnerabilities.

## Disclaimer

VulnHunt-GPT is a research-oriented tool and should not be solely relied upon for critical security decisions. Always perform additional security audits and reviews.

---

### Contact

For questions or support, please reach out to the project maintainer at quynhnhu170218@gmail.com.

