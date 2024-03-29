from settings import INSTALLED_APPS
from functools import reduce

def get_server_actions():
	modules = reduce(
			lambda value, item: value + [__import__(f'{item}.actions')],
			INSTALLED_APPS,
			[],
	)
	actions = reduce(
			lambda value, item: value + [getattr(item, 'actions', [])],
			modules,
			[],
	)

	return reduce(
			lambda value, item: value + getattr(item, 'action_names', []),
			actions,
			[],
	)


def resolve(action_name, actions=None):
	action_list = actions or get_server_actions()
	action_map = {
		action.get('action'):action.get('controller')
		for action in action_list
	}
	return action_map.get(action_name)

