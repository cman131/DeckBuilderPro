Feature List:
Stage 1:
	Search Decks:
	 - Criteria:
	  - SearchTerm = is contained within title and/or description of deck
	  - Colors = The deck will have these colors and no others
	  - Creator = the user who created the deck
	 - Can only view public decks
	Create Decks:
	 - Decks can have up to 1000 cards
	 - Deck Properties:
	  - Name
	  - Description
	  - Color = the colors contained within the deck
	  - Size = the number of cards
	  - List of Cards with counts within deck
Stage 2:
	Local Cards:
	 - Card Table
	 - Only update db from mtgjson
	 - No more frontloaded JS
	 - Deck_Card "cardId" become foreign keys of the "Card" table "id"
	 - Deckbuilder source from local db
	Register
	 - User Properties:
	  - Unique username
	  - Unique email address
	  - Salted and Hashed Password
	 Login
	  - The User can log in
	  - a session that persists multiple pages will be created
	  - Deckbuilder decks marked by creating user

Stage 3:
	Collection:
	 - Collection Management Page:
	  - Add to collection
	  - Remove from collection
	  - View Collection
	 DeckBuilder from Collection:
	  - Available cards sourced from user collection
