"""Game mixins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.views import OrderablePaginatedListView
from project_manager.games.models import Game


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GameSpecificOrderablePaginatedListView',
)


# =============================================================================
# >> MIXINS
# =============================================================================
class GameSpecificOrderablePaginatedListView(OrderablePaginatedListView):
    """View to be inherited for ordering, pagination, and game filtering."""

    def get_queryset(self):
        """Filter to projects that support the given game."""
        queryset = super().get_queryset()
        basename = self.request.GET.get('game')
        if basename is not None:
            return queryset.filter(supported_games__basename__exact=basename)
        return queryset

    def get_context_data(self, **kwargs):
        """Add all the proper context for templates."""
        context = super().get_context_data(**kwargs)
        game_slug = self.request.GET.get('game')
        games = Game.objects.order_by(
            'name'
        ).values(
            'slug',
            'name',
        )
        game_name = {
            game['slug']: game['name'] for game in games
        }.get(game_slug)
        context.update({
            'game_name': game_name,
            'games': games,
            'game_slug': game_slug,
        })
        if game_name:
            for num, item in enumerate(context['page_url_list']):
                if item.url is None:
                    continue
                context['page_url_list'][num].url = context[
                    'page_url_list'
                ][num].url + f'&game={game_slug}'
        return context
