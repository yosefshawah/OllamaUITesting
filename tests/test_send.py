import pytest
from pages.ollama_chat_page import OllamaChatPage

class TestOllamaChat:
    
    def test_select_model_and_send_prompt(self, driver, base_url):
        """Test selecting a model and sending a prompt to get a response"""
        test_message = "hello world"
        
        # Initialize page object and chain the entire flow
        chat_page = (OllamaChatPage(driver)
                    .navigate_to(base_url)
                    .clear_app_state()
                    .select_model()
                    .enter_prompt(test_message))
        
        # Verify the text was entered correctly
        assert test_message in chat_page.get_prompt_value(), "Prompt text was not entered correctly"
        
        # Submit and get response using chaining
        chat_page.submit_prompt()
        response_texts = chat_page.wait_for_response()
        
        # Print the response for debugging
        print("Model response:")
        for line in response_texts:
            print("-", line)
        
        # Assert that we got a response
        assert len(response_texts) > 0, "No response paragraphs found from the model"
