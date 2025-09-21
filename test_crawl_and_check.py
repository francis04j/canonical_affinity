import pytest
from semantic_search import find_semantic_url_matches

def test_find_semantic_url_matches_positive_case():
    html_chunks = [
        "This is a sample HTML chunk about machine learning.",
        "Another chunk discussing artificial intelligence.",
        "Completely unrelated content about cooking recipes."
    ]
    target_url = "https://trainline.com/machine-learning-and-ai"
    matches = find_semantic_url_matches(html_chunks, target_url, similarity_threshold=0.1)
    assert len(matches) > 0
    assert matches[0][0] == "This is a sample HTML chunk about machine learning."

def test_find_semantic_url_matches_empty_html_chunks():
    html_chunks = []
    target_url = "https://trainline.com/machine-learning-and-ai"
    matches = find_semantic_url_matches(html_chunks, target_url)
    assert matches == []

def test_find_semantic_url_matches_no_matches():
    html_chunks = [
        "Completely unrelated content about cooking recipes.",
        "Another chunk discussing gardening tips."
    ]
    target_url = "https://trainline.com/machine-learning-and-ai"
    matches = find_semantic_url_matches(html_chunks, target_url, similarity_threshold=0.5)
    assert matches == []

def test_find_semantic_url_matches_high_threshold():
    html_chunks = [
        "This is a sample HTML chunk about machine learning.",
        "Another chunk discussing artificial intelligence."
    ]
    target_url = "https://trainline.com/machine-learning-and-ai"
    matches = find_semantic_url_matches(html_chunks, target_url, similarity_threshold=0.99)
    assert matches == []

def test_find_semantic_url_matches_invalid_inputs():
    html_chunks = [123, None, "Valid chunk"]
    target_url = "https://trainline.com/machine-learning-and-ai"
    with pytest.raises(Exception):
        find_semantic_url_matches(html_chunks, target_url)

def test_find_semantic_url_matches_partial_match():
    html_chunks = [
        "This is a sample HTML chunk about AI.",
        "Another chunk discussing machine learning.",
        "Completely unrelated content about cooking recipes."
    ]
    target_url = "https://trainline.com/machine-learning-and-ai"
    matches = find_semantic_url_matches(html_chunks, target_url, similarity_threshold=0.1)
    assert len(matches) > 0
    assert any("machine learning" in match[0] for match in matches)

def test_find_semantic_url_matches_all_chunks_match():
    html_chunks = [
        "This is a sample HTML chunk about machine learning.",
        "Another chunk discussing artificial intelligence.",
        "Machine learning and AI are closely related fields."
    ]
    target_url = "https://trainline.com/machine-learning-and-ai"
    matches = find_semantic_url_matches(html_chunks, target_url, similarity_threshold=0.1)
    assert len(matches) == len(html_chunks)

def test_find_semantic_url_matches_no_scheme_in_target_url():
    html_chunks = [
        "This is a sample HTML chunk about machine learning.",
        "Another chunk discussing artificial intelligence."
    ]
    target_url = "trainline.com/machine-learning-and-ai"
    matches = find_semantic_url_matches(html_chunks, target_url, similarity_threshold=0.1)
    assert len(matches) > 0
    assert matches[0][0] == "This is a sample HTML chunk about machine learning."