"""
Test Oracle AI functionality
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from synesthesia.llm.oracle_ai import OracleAI

load_dotenv()

# Create mock simulation state
mock_state = {
    'agents': [
        {
            'id': 0,
            'name': 'Emma Johnson',
            'age': 28,
            'role': 'teacher',
            'mental_health': {
                'anxiety': 0.85,
                'depression': 0.45,
                'stress': 0.92,
                'wellbeing': 0.25,
                'category': 'crisis'
            }
        },
        {
            'id': 1,
            'name': 'Liam Smith',
            'age': 32,
            'role': 'teacher',
            'mental_health': {
                'anxiety': 0.72,
                'depression': 0.38,
                'stress': 0.78,
                'wellbeing': 0.35,
                'category': 'struggling'
            }
        },
        {
            'id': 2,
            'name': 'Olivia Brown',
            'age': 19,
            'role': 'student',
            'mental_health': {
                'anxiety': 0.45,
                'depression': 0.25,
                'stress': 0.55,
                'wellbeing': 0.65,
                'category': 'coping'
            }
        },
        {
            'id': 3,
            'name': 'Noah Davis',
            'age': 20,
            'role': 'student',
            'mental_health': {
                'anxiety': 0.25,
                'depression': 0.15,
                'stress': 0.35,
                'wellbeing': 0.85,
                'category': 'thriving'
            }
        },
        {
            'id': 4,
            'name': 'Ava Wilson',
            'age': 18,
            'role': 'student',
            'mental_health': {
                'anxiety': 0.35,
                'depression': 0.20,
                'stress': 0.45,
                'wellbeing': 0.75,
                'category': 'thriving'
            }
        }
    ],
    'stats': {
        'thriving': 2,
        'coping': 1,
        'struggling': 1,
        'crisis': 1
    },
    'time': '2024-03-15 14:30:00'
}

def test_oracle():
    """Test Oracle AI with sample queries"""
    
    print("\n" + "="*60)
    print("🔮 TESTING ORACLE AI")
    print("="*60)
    
    # Initialize Oracle
    llm_client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )
    
    oracle = OracleAI(llm_client)
    
    # Test queries
    queries = [
        "Who is most at risk right now?",
        "What are the main mental health trends?",
        "Which roles are most stressed?",
        "What interventions would help?"
    ]
    
    for i, question in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"QUERY {i}: {question}")
        print("="*60)
        
        try:
            result = oracle.query(question, mock_state)
            
            print(f"\n📝 ANSWER:")
            print(result['answer'])
            
            if result.get('statistics'):
                print(f"\n📊 STATISTICS:")
                for key, value in result['statistics'].items():
                    print(f"  • {key}: {value}")
            
            if result.get('insights'):
                print(f"\n💡 INSIGHTS:")
                for insight in result['insights']:
                    print(f"  • {insight}")
            
            if result.get('recommendations'):
                print(f"\n🎯 RECOMMENDATIONS:")
                for rec in result['recommendations']:
                    print(f"  • {rec}")
            
            if result.get('agents_of_interest'):
                print(f"\n👥 AGENTS OF INTEREST:")
                for agent in result['agents_of_interest']:
                    print(f"  • {agent['name']}: {agent['reason']}")
        
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ ORACLE AI TEST COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_oracle()
