# -*- coding: utf-8 -*-

import plum.workflow
from aiida.work.process import Process
from aiida.orm import load_node


__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file."
__authors__ = "The AiiDA team."
__version__ = "0.7.1"


class Workflow(Process, plum.workflow.Workflow):
    """
    This class represents an AiiDA workflow which can be executed and will
    have full provenance saved in the database.
    """

    _CHILD_LABEL = '__label'
    _INPUT_BUFFER = '__input_buffer'
    _spec_type = plum.workflow.WorkflowSpec

    def _create_child_record(self, child, inputs):
        # Find the child
        child_label = self._find_instance_label(child)
        assert child_label

        child_record = super(Workflow, self)._create_child_record(child, inputs)
        child_record.instance_state[self._CHILD_LABEL] = child_label
        return child_record

    def _find_instance_label(self, process):
        inst_label = None
        for label, proc in self._process_instances.iteritems():
            if proc is process:
                inst_label = label
                break
        return inst_label

    # Messages #####################################################
    def _on_value_buffered(self, link, value):
        super(Workflow, self)._on_value_buffered(link, value)

        state = self._process_record.instance_state.setdefault(
            self._INPUT_BUFFER, {})
        state[str(link)] = value
        self._process_record.save()

    def _on_value_consumed(self, link, value):
        super(Workflow, self)._on_value_consumed(link, value)

        state = self._process_record.instance_state[self._INPUT_BUFFER]
        state.pop(str(link))
        self._process_record.save()
    ################################################################
