/*
 * Copyright (c) 2014, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 */
/**
 * \file
 *         A process that periodically prints out the time spent in
 *         radio tx, radio rx, total time and duty cycle.
 *
 * \author Simon Duquennoy <simonduq@sics.se>
 */

#include "contiki.h"
#include "node-id.h"
#include "simple-energest.h"
#include <stdio.h>
#include "deployment-log.h"

static uint32_t last_tx, last_rx, last_time;
static uint32_t delta_tx, delta_rx, delta_time;
static uint32_t curr_tx, curr_rx, curr_time;

/*---------------------------------------------------------------------------*/
void
simple_energest_init()
{
    energest_flush();
    last_tx = energest_type_time(ENERGEST_TYPE_TRANSMIT);
    last_rx = energest_type_time(ENERGEST_TYPE_LISTEN);
    last_time = energest_type_time(ENERGEST_TYPE_CPU) + energest_type_time(ENERGEST_TYPE_LPM);
}
/*---------------------------------------------------------------------------*/
void
simple_energest_step(int verbose)
{
    static uint16_t cnt;
    energest_flush();

    curr_tx = energest_type_time(ENERGEST_TYPE_TRANSMIT);
    curr_rx = energest_type_time(ENERGEST_TYPE_LISTEN);
    curr_time = energest_type_time(ENERGEST_TYPE_CPU) + energest_type_time(ENERGEST_TYPE_LPM);

    delta_tx = curr_tx - last_tx;
    delta_rx = curr_rx - last_rx;
    delta_time = curr_time - last_time;

    last_tx = curr_tx;
    last_rx = curr_rx;
    last_time = curr_time;

    if(verbose) {
        uint32_t fraction = (1000ul * (delta_tx + delta_rx)) / delta_time;
        LOG("Duty Cycle: [%u %u] %8lu +%8lu /%8lu (%lu permil)\n",
            node_id,
            cnt++,
            delta_tx, delta_rx, delta_time,
            fraction
        );
    }
}
