from pathlib import Path
import ui

root_dir = Path.expanduser(Path('~/Documents'))
purge_name = [
  'site-packages',
  'site-packages-2',
  'site-packages-3',
  '.DS_Store',
  '.Trash',
  '.pythonista_pytest_log.xml',
  '.style.yapf',
  '.tabs.bak',
  '.tabs.dat',
  '.tabs.dir',
  'Examples',
  'Templates',
]


class FolderBrowser:
  def __init__(self):
    # todo: 繰り返し防止考える
    self.btn_done = ui.ButtonItem(title='Done')
    self.btn_done.action = self.get_done
    init_table = ui.TableView()
    list_source = ui.ListDataSource(self.create_list(root_dir))
    list_source.action = self.select_cell
    init_table.data_source = list_source
    init_table.delegate = list_source
    init_table.name = self.call_dir.name
    self.activ_table = init_table
    self.activ_table.right_button_items = [self.btn_done]
    self.nav = ui.NavigationView(self.activ_table)

    # todo: Home に戻る
    home = ui.ButtonItem()
    home.image = ui.Image.named('Home')
    home.action = self.goto_home
    self.nav.left_button_items = [home]
    # todo: icon サイズ違う、、、、
    new = ui.ButtonItem()
    new.image = ui.Image.named('FolderNew')
    new.action = self.new_folder
    self.nav.right_button_items = [new]

  def create_list(self, root_path):
    self.call_dir = root_path
    # todo: if文 ダサい
    if self.call_dir != root_dir:
      dirs = sorted([d for d in self.call_dir.iterdir() if d.is_dir()])
    else:
      dirs = sorted([
        d for d in self.call_dir.iterdir()
        if d.is_dir() and str(d.name) not in purge_name
      ])

    set_items = []
    for dir in dirs:
      set_items.append({
        'title': dir.name,
        'image': ui.Image.named('Folder'),
        'path': dir
      })
    return set_items

  def select_cell(self, sender):
    selection = sender.items[sender.selected_row]
    # todo: 繰り返し防止考える
    slct_dir = selection['path']
    slct_list_source = ui.ListDataSource(self.create_list(slct_dir))
    slct_table = ui.TableView()
    slct_list_source.action = self.select_cell
    slct_table.data_source = slct_list_source
    slct_table.delegate = slct_list_source
    slct_table.name = selection['title']
    self.activ_table = slct_table
    self.activ_table.right_button_items = [self.btn_done]
    self.nav.push_view(self.activ_table)

  def goto_home(self, sender):
    # todo: この戻り方でええのか？
    home_list_source = ui.ListDataSource(self.create_list(root_dir))
    home_table = ui.TableView()
    home_list_source.action = self.select_cell
    home_table.data_source = home_list_source
    home_table.delegate = home_list_source
    home_table.name = root_dir.name
    self.activ_table = home_table
    self.activ_table.right_button_items = [self.btn_done]
    self.nav.push_view(self.activ_table)

  def new_folder(self, sender):
    # todo: なまえつける
    Path(self.call_dir / 'hoge').mkdir(exist_ok=True)
    nf_list_source = ui.ListDataSource(self.create_list(self.call_dir))
    nf_list_source.action = self.select_cell
    self.activ_table.delegate = nf_list_source
    self.activ_table.data_source = nf_list_source
    self.activ_table.reload()

  def get_done(self, sender):
    print(self.call_dir)

  def show_browser(self):
    #self.nav.name = 'Choose directly ...'
    self.nav.present()  #hide_title_bar=True)


fb = FolderBrowser()
fb.show_browser()

