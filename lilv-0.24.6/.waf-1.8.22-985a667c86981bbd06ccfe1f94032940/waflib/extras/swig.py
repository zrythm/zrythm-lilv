#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import re
from waflib import Task,Logs
from waflib.TaskGen import extension
from waflib.Configure import conf
from waflib.Tools import c_preproc
SWIG_EXTS=['.swig','.i']
re_module=re.compile('%module(?:\s*\(.*\))?\s+(.+)',re.M)
re_1=re.compile(r'^%module.*?\s+([\w]+)\s*?$',re.M)
re_2=re.compile('[#%]include [<"](.*)[">]',re.M)
class swig(Task.Task):
	color='BLUE'
	run_str='${SWIG} ${SWIGFLAGS} ${SWIGPATH_ST:INCPATHS} ${SWIGDEF_ST:DEFINES} ${SRC}'
	ext_out=['.h']
	vars=['SWIG_VERSION','SWIGDEPS']
	def runnable_status(self):
		for t in self.run_after:
			if not t.hasrun:
				return Task.ASK_LATER
		if not getattr(self,'init_outputs',None):
			self.init_outputs=True
			if not getattr(self,'module',None):
				txt=self.inputs[0].read()
				m=re_module.search(txt)
				if not m:
					raise ValueError("could not find the swig module name")
				self.module=m.group(1)
			swig_c(self)
			for x in self.env['SWIGFLAGS']:
				x=x[1:]
				try:
					fun=swig_langs[x]
				except KeyError:
					pass
				else:
					fun(self)
		return super(swig,self).runnable_status()
	def scan(self):
		lst_src=[]
		seen=[]
		to_see=[self.inputs[0]]
		while to_see:
			node=to_see.pop(0)
			if node in seen:
				continue
			seen.append(node)
			lst_src.append(node)
			code=node.read()
			code=c_preproc.re_nl.sub('',code)
			code=c_preproc.re_cpp.sub(c_preproc.repl,code)
			names=re_2.findall(code)
			for n in names:
				for d in self.generator.includes_nodes+[node.parent]:
					u=d.find_resource(n)
					if u:
						to_see.append(u)
						break
				else:
					Logs.warn('could not find %r'%n)
		return(lst_src,[])
swig_langs={}
def swigf(fun):
	swig_langs[fun.__name__.replace('swig_','')]=fun
swig.swigf=swigf
def swig_c(self):
	ext='.swigwrap_%d.c'%self.generator.idx
	flags=self.env['SWIGFLAGS']
	if'-c++'in flags:
		ext+='xx'
	out_node=self.inputs[0].parent.find_or_declare(self.module+ext)
	if'-c++'in flags:
		c_tsk=self.generator.cxx_hook(out_node)
	else:
		c_tsk=self.generator.c_hook(out_node)
	c_tsk.set_run_after(self)
	ge=self.generator.bld.producer
	ge.outstanding.insert(0,c_tsk)
	ge.total+=1
	try:
		ltask=self.generator.link_task
	except AttributeError:
		pass
	else:
		ltask.set_run_after(c_tsk)
		ltask.inputs.append(c_tsk.outputs[0])
	self.outputs.append(out_node)
	if not'-o'in self.env['SWIGFLAGS']:
		self.env.append_value('SWIGFLAGS',['-o',self.outputs[0].abspath()])
@swigf
def swig_python(tsk):
	node=tsk.inputs[0].parent
	if tsk.outdir:
		node=tsk.outdir
	tsk.set_outputs(node.find_or_declare(tsk.module+'.py'))
@swigf
def swig_ocaml(tsk):
	node=tsk.inputs[0].parent
	if tsk.outdir:
		node=tsk.outdir
	tsk.set_outputs(node.find_or_declare(tsk.module+'.ml'))
	tsk.set_outputs(node.find_or_declare(tsk.module+'.mli'))
@extension(*SWIG_EXTS)
def i_file(self,node):
	tsk=self.create_task('swig')
	tsk.set_inputs(node)
	tsk.module=getattr(self,'swig_module',None)
	flags=self.to_list(getattr(self,'swig_flags',[]))
	tsk.env.append_value('SWIGFLAGS',flags)
	tsk.outdir=None
	if'-outdir'in flags:
		outdir=flags[flags.index('-outdir')+1]
		outdir=tsk.generator.bld.bldnode.make_node(outdir)
		outdir.mkdir()
		tsk.outdir=outdir
@conf
def check_swig_version(conf,minver=None):
	assert minver is None or isinstance(minver,tuple)
	swigbin=conf.env['SWIG']
	if not swigbin:
		conf.fatal('could not find the swig executable')
	cmd=swigbin+['-version']
	Logs.debug('swig: Running swig command %r',cmd)
	reg_swig=re.compile(r'SWIG Version\s(.*)',re.M)
	swig_out=conf.cmd_and_log(cmd)
	swigver_tuple=tuple([int(s)for s in reg_swig.findall(swig_out)[0].split('.')])
	result=(minver is None)or(swigver_tuple>=minver)
	if result:
		swigver='.'.join([str(x)for x in swigver_tuple[:2]])
		conf.env['SWIG_VERSION']=swigver
	swigver_full='.'.join(map(str,swigver_tuple[:3]))
	if minver is None:
		conf.msg('Checking for swig version',swigver_full)
	else:
		minver_str='.'.join(map(str,minver))
		conf.msg('Checking for swig version >= %s'%(minver_str,),swigver_full,color=result and'GREEN'or'YELLOW')
	if not result:
		conf.fatal('The swig version is too old, expecting %r'%(minver,))
	return swigver_tuple
def configure(conf):
	conf.find_program('swig',var='SWIG')
	conf.env.SWIGPATH_ST='-I%s'
	conf.env.SWIGDEF_ST='-D%s'