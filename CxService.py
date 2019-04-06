import json
import CxRest


class CxService(object):

    unknown_id = -1
    unknown_id_str = "-1"
    source_artifact = "SourceArtifact"
    build_artifact = "BuildArtifact"

    def __init__(self, server, username, password, cx_config):
        self.server = server
        self.username = username
        self.password = password
        self.cx_config = cx_config
        self.cx = CxRest.CxRestClient(server, username, password, cx_config)
        pass

    def get_preset_id(self, preset):
        presets = self.cx.get_all_preset_details().json()
        for p in presets:
            if p['name'] == preset:
                return p['id']

        return CxService.unknown_id

    def get_team_id(self, team):
        teams = self.cx.get_all_teams().json()
        for t in teams:
            if t['fullName'] == team:
                return t['id']
        return CxService.unknown_id_str

    def get_configuration_id(self, configuration):
        configs = self.cx.get_all_engine_configurations().json()
        for c in configs:
            if c['name'] == configuration:
                return c['id']
        return CxService.unknown_id

    def get_project_id(self, team_id, project):
        projects = self.cx.get_all_projects().json()
        for p in projects:
            if p['teamId'] == team_id and p['name'] == project:
                return p['id']
        return CxService.unknown_id

    def start_scan(self, cx_config):
        preset = self.get_preset_id(cx_config['preset'])
        if preset == CxService.unknown_id:
            raise Exception(" Unknown preset " + cx_config['preset'])

        team = self.get_team_id(cx_config['team'])
        if preset == CxService.unknown_id_str:
            raise Exception(" Unknown team name" + cx_config['team'])

        config = self.get_configuration_id(cx_config['configuration'])
        if preset == CxService.unknown_id:
            raise Exception(" Unknown Scan Configuration " + cx_config['configuration'])

        project = self.get_project_id(team, cx_config['project'])
        # create project if doesn't exist
        if project == CxService.unknown_id:
            prj = self.cx.create_project_with_default_configuration(name=cx_config['project'], owning_team=team,
                                                                    is_public=True).json()
            project = prj['id']
        self.cx.update_sast_scan_settings(project, preset, config)
        self.cx.upload_source_code_zip_file(project, cx_config['file'])
        self.cx.create_new_scan(project)

    @staticmethod
    def get_urls():
        try:
            with open("urls.json") as urls:
                return json.loads(urls.read())
        except Exception as e:
            raise Exception("Unable to get configuration: {} . ".format(e))


