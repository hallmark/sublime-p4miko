import sublime, sublime_plugin
import os, sys, socket
try:
  import paramiko
except ImportError:
  sublime.status_message('Install paramiko locally to enable p4miko plugin')

plugin_settings = sublime.load_settings('p4miko.sublime-settings')
ssh_host = sublime.active_window().active_view().settings().get('perforce_ssh_host', plugin_settings.get('perforce_ssh_host'))
local_client_prefix = os.path.normpath(sublime.active_window().active_view().settings().get('perforce_local_client_prefix', plugin_settings.get('perforce_local_client_prefix')))
remote_prefix = sublime.active_window().active_view().settings().get('perforce_ssh_remote_client_prefix', plugin_settings.get('perforce_ssh_remote_client_prefix'))

def get_project_prefix(window):
  project_prefix = window.active_view().settings().get('perforce_remote_project_prefix', plugin_settings.get('perforce_remote_project_prefix'))
  return project_prefix

def derive_remote_path(local_path):
  local_path = os.path.normpath(local_path)
  if (not local_path.startswith(local_client_prefix)):
    sublime.status_message('File not part of project: ' + local_path)
    raise Exception('command aborted')
  relpath = os.path.relpath(local_path, local_client_prefix)
  remote_path = os.path.join(remote_prefix, relpath)
  return remote_path

def execute_paramiko_command(command):
  print command
  client = None
  try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    try:
      client.connect(ssh_host)
    except socket.gaierror as e:
      sublime.status_message('Unable to lookup SSH host')
      # sublime.message_dialog('Unable to lookup SSH host')
      return '', ''

    stdin, stdout, stderr = client.exec_command(command)
    stdin.close()
    return stdout.read(), stderr.read()

  finally:
    if client:
      client.close()

# Subclass this for commands that require focus on a file
class P4MikoProjectFileCommand(sublime_plugin.TextCommand):
  def is_enabled(self):
    return (self.view.file_name() is not None)

  def log_command_output(self, output, err, cmd_name):
    if err:
      print '(p4miko) p4 ' + cmd_name + ' err:'
      out_lines = err.splitlines()
      for line in out_lines:
        print line
    elif output:
      print '(p4miko) p4 ' + cmd_name + ' output:'
      out_lines = output.splitlines()
      for line in out_lines:
        print line
    else:
      print '(p4miko) no out/err output from p4 ' + cmd_name


  def run(self, edit):
    sublime.message_dialog('This command is not intended to be run directly. Subclass and override run().')

class P4MikoAddCommand(P4MikoProjectFileCommand):
  def run(self, edit):
    print 'p4miko - Invoking p4 add for file: ' + self.view.file_name()
    remote_path = derive_remote_path(self.view.file_name())
    output, err = execute_paramiko_command('p4 add ' + remote_path)

    self.log_command_output(output, err, 'add')

    out_lines = output.splitlines()
    if out_lines:
      status = out_lines[0]
      if status.endswith('currently opened for add'):
        sublime.status_message('p4: file already opened for add')
      elif status.endswith('opened for add'):
        sublime.status_message('p4: file opened for add')
      elif status.endswith('can\'t add existing file'):
        sublime.status_message('p4: file already exists in repo')
      elif status.endswith('can\'t add (already opened for edit)'):
        sublime.status_message('p4: file already exists in repo')
      else:
        sublime.status_message('p4: unable to add file: ' + status)
    else:
      sublime.status_message('p4: no output from p4 add')

class P4MikoFilelogCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print 'p4miko - Invoking p4 filelog for file: ' + self.view.file_name()
    sublime.status_message('filelog not yet implemented')

#
class P4MikoDiffCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print 'p4miko - Invoking p4 diff for file: ' + self.view.file_name()
    sublime.status_message('diff not yet implemented')

#
class P4MikoRevertCommand(sublime_plugin.TextCommand):
  def is_enabled(self):
    return (self.view.file_name() is not None)

  def run(self, edit):
    # file_name = os.path.basename(self.view.file_name())
    relpath = os.path.relpath(self.view.file_name(), local_client_prefix)

    if sublime.ok_cancel_dialog('Are you sure you want to revert file ' + relpath, 'Revert'):
      print 'p4miko - Invoking p4 revert for file: ' + self.view.file_name()
      remote_path = derive_remote_path(self.view.file_name())
      output, err = execute_paramiko_command("echo 'y' | p4 revert " + remote_path)

      print 'p4miko - p4 revert output:'
      out_lines = output.splitlines()
      for line in out_lines:
        print line
      if out_lines:
        status = out_lines[0]
        if status.endswith('was edit, reverted'):
          sublime.status_message('p4: file reverted, no longer open for edit')
        elif status.endswith('was add, abandoned'):
          sublime.status_message('p4: file reverted, no longer added')
        elif status.endswith('file(s) not opened on this client.'):
          sublime.status_message('p4: file not opened on client')
        else:
          sublime.status_message('p4: unable to revert file: ' + status)
      else:
        sublime.status_message('p4: no output from p4 revert')


class P4MikoEditCommand(P4MikoProjectFileCommand):
  def run(self, edit):
    print 'p4miko - Invoking p4 edit for file: ' + self.view.file_name()
    remote_path = derive_remote_path(self.view.file_name())
    output, err = execute_paramiko_command('p4 edit ' + remote_path)

    self.log_command_output(output, err, 'edit')

    if err:
      out_lines = err.splitlines()
      status = out_lines[0]
      if status.endswith('file(s) not on client.'):
        sublime.status_message('p4: cannot edit file that has not been added')
      else:
        sublime.status_message('p4: unable to open file for edit: ' + status)
    elif output:
      out_lines = output.splitlines()
      status = out_lines[0]
      if status.endswith('currently opened for edit'):
        sublime.status_message('p4: file already opened for edit')
      elif status.endswith('opened for edit'):
        sublime.status_message('p4: file opened for edit')
      else:
        sublime.status_message('p4: unable to open file for edit: ' + status)
    else:
      sublime.status_message('p4: no output from p4 edit')

class P4MikoOpenedCommand(sublime_plugin.WindowCommand):
  def run(self):
    project_prefix = get_project_prefix(self.window)
    if project_prefix is None:
      sublime.message_dialog('Not in project or project not configured with "perforce_remote_project_prefix" setting.')
      return
    print 'p4miko - Invoking p4 opened for current project: ' + project_prefix
    output, err = execute_paramiko_command('p4 -d ' + project_prefix + ' opened ...')

    print 'p4miko - p4 opened output:'
    out_lines = output.splitlines()
    for line in out_lines:
      print line
    sublime.active_window().show_quick_panel(out_lines, lambda x: None)



