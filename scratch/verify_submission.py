import os
from pptx import Presentation

pptx_path = 'submission/StallBreaker_TekQubit_2026_Final_Pitch.pptx'
notes_path = 'submission/StallBreaker_Pitch_Speaker_Notes.md'
review_path = 'submission/StallBreaker_Six_Agent_Review.md'

assert os.path.exists(pptx_path), 'pptx missing'
assert os.path.exists(notes_path), 'notes missing'
assert os.path.exists(review_path), 'review missing'

prs = Presentation(pptx_path)
print(f'PPTX verified: {len(prs.slides)} slides')

banned = ['$10,000', '$1,200', '<800 ms', '100% achievable', '100% operational executability', 'first dealership recovery architecture']

with open(notes_path, 'r', encoding='utf-8') as f:
    notes_text = f.read()

with open(review_path, 'r', encoding='utf-8') as f:
    review_text = f.read()

pptx_text = ''
for s in prs.slides:
    for shp in s.shapes:
        if shp.has_text_frame:
            pptx_text += shp.text_frame.text + ' '

for b in banned:
    in_pptx = b.lower() in pptx_text.lower()
    in_notes = b.lower() in notes_text.lower()
    in_rev = b.lower() in review_text.lower()
    print(f'Check "{b}": in_pptx={in_pptx}, in_notes={in_notes}, in_review={in_rev}')

print("ALL VERIFICATIONS COMPLETED.")
